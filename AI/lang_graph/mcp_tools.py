"""Connect a LangGraph agent to a remote MCP server and let the LLM use its tools.

A LangGraph tool-calling loop: the [agent] node binds the tools discovered on a
live MCP server (streamable HTTP) and calls the LLM; when the LLM asks for a
tool, the [tools] node executes it over MCP and feeds the result back. The loop
ends when the LLM answers without requesting a tool.

    uv run mcp_tools.py
    uv run mcp_tools.py "<question>"

Prereqs: LM Studio on http://localhost:1234 and the MCP server on
http://127.0.0.1:8000/mcp must both be running.
"""

import asyncio
import sys

from langchain_core.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, MessagesState, StateGraph

sys.stdout.reconfigure(encoding="utf-8")

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)

MCP_URL = "http://127.0.0.1:8000/mcp"

client = MultiServerMCPClient(
    {"support": {"url": MCP_URL, "transport": "streamable_http"}}
)

# get_tools() opens a session, lists the server's tools, and closes it. Each
# returned tool reconnects on its own when invoked, so we fetch once here and
# reuse the tool objects for the lifetime of the process.
tools = asyncio.run(client.get_tools())
tools_by_name = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)


async def agent(state: MessagesState) -> dict:
    print(f"[agent] calling LLM (messages={len(state['messages'])})")
    response = await llm_with_tools.ainvoke(state["messages"])
    if response.tool_calls:
        names = ", ".join(tc["name"] for tc in response.tool_calls)
        print(f"[agent] LLM requested tool(s): {names}")
    else:
        print("[agent] LLM produced a final answer (no tool calls)")
    return {"messages": [response]}


async def call_tools(state: MessagesState) -> dict:
    results = []
    for tc in state["messages"][-1].tool_calls:
        print(f"[tools] executing MCP tool '{tc['name']}' args={tc['args']}")
        output = await tools_by_name[tc["name"]].ainvoke(tc["args"])
        results.append(ToolMessage(content=str(output), tool_call_id=tc["id"], name=tc["name"]))
    return {"messages": results}


def route(state: MessagesState) -> str:
    return "tools" if state["messages"][-1].tool_calls else END


workflow = StateGraph(MessagesState)

workflow.add_node("agent", agent)
workflow.add_node("tools", call_tools)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", route, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

graph = workflow.compile()
png_bytes = graph.get_graph(xray=1).draw_mermaid_png()
with open("mcp_tools.png", "wb") as f:
    f.write(png_bytes)


async def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else "What is my current IP address and Wi-Fi network?"

    print("--- TOOLS DISCOVERED ON MCP SERVER ---")
    for t in tools:
        print(f"  {t.name}: {(t.description or '').splitlines()[0]}")
    print("--- /TOOLS ---\n")

    result = await graph.ainvoke({"messages": [{"role": "user", "content": question}]})

    print("\n--- ANSWER ---")
    print(result["messages"][-1].content)
    print("--- /ANSWER ---")


if __name__ == "__main__":
    asyncio.run(main())
