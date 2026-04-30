import json
from typing import Annotated

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel


# 1. define LLM
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)


# 2. create tools
class WeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "Return current weather for a city."

    def _run(self, city: str) -> str:
        return f"The weather in {city} is sunny and 75°F."


class TranslateTool(BaseTool):
    name: str = "translate_text"
    description: str = "Translate English text to Spanish."

    def _run(self, text: str) -> str:
        return f"Spanish translation of '{text}': 'Hola mundo!'"


class SummarizeTool(BaseTool):
    name: str = "summarize_article"
    description: str = "Summarize a long article."

    def _run(self, article: str) -> str:
        return f"Summary: {article[:60]}..."


TOOLS = [
    WeatherTool(),
    TranslateTool(),
    SummarizeTool(),
]


# 3. bind tools to model
tool_enabled_llm = llm.bind_tools(TOOLS)


# 4. create safe list
SAFE_TOOLS = {
    "get_weather",
}


# 5. define state
class State(BaseModel):
    messages: Annotated[list, add_messages]

    # router writes here
    next_step: str | None = None


# 6. define nodes
def llm_node(state: State):
    print("\n=== User ===")
    print(state.messages[-1].content)

    response = tool_enabled_llm.invoke(state.messages)

    if not response.tool_calls:
        raise RuntimeError("LLM did not select a tool.")

    tool_call = response.tool_calls[0]

    print("\n=== LLM selected ===")
    print(tool_call["name"])
    print(
        json.dumps(
            tool_call["args"],
            indent=2,
        )
    )

    return {
        "messages": [response],
    }


def router_node(state: State):
    last_ai: AIMessage = state.messages[-1]

    tool_name = last_ai.tool_calls[0]["name"]

    next_step = "auto_execute" if tool_name in SAFE_TOOLS else "hitl"

    print("\n=== Router ===")
    print(f"{tool_name} -> {next_step}")

    return {
        "next_step": next_step,
    }


def hitl_node(state: State):
    last_ai: AIMessage = state.messages[-1]

    tool_call = last_ai.tool_calls[0]

    print("\n=== HITL ===")
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")

    confirm = input("Proceed? (y/n): ").strip().lower()

    if confirm != "y":
        print("\nExecution aborted.")

        raise RuntimeError("User denied tool execution.")

    print("\nApproved.")

    return {}


# 7. use Tool node to run tools
tool_node = ToolNode(TOOLS)


# 8. build graph
graph = StateGraph(state_schema=State)

graph.add_node("llm", llm_node)
graph.add_node("router", router_node)
graph.add_node("hitl", hitl_node)
graph.add_node("auto_execute", tool_node)
graph.add_node("manual_execute", tool_node)

graph.add_edge(START, "llm")
graph.add_edge("llm", "router")
graph.add_conditional_edges(
    "router",
    lambda state: state.next_step or "hitl",
    {
        "auto_execute": "auto_execute",
        "hitl": "hitl",
    },
)
graph.add_edge("hitl", "manual_execute")
graph.add_edge("auto_execute", END)
graph.add_edge("manual_execute", END)

app = graph.compile()
png_bytes = app.get_graph().draw_mermaid_png()
with open("hitl_advanced.png", "wb") as f:
    f.write(png_bytes)


# 9. Glue everything together
def run_query(user_input: str):
    print("\n" + "=" * 60)

    result = app.invoke({"messages": [HumanMessage(content=user_input)]})

    print("\n=== Final Messages ===")

    for msg in result["messages"]:
        print(
            "\n---",
            type(msg).__name__,
            "---",
        )

        if hasattr(msg, "content"):
            print(msg.content)


def main():

    demo_inputs = [
        # auto
        ("What's the weather in San Francisco?"),
        # HITL
        ("Translate 'Hello world' to Spanish."),
        # HITL
        (
            "Summarize this article: "
            "Artificial intelligence is "
            "rapidly transforming industries..."
        ),
    ]

    for query in demo_inputs:
        run_query(query)


if __name__ == "__main__":
    main()
