"""Importing a subgraph across files and dropping it into a parent graph.

`letter_counter.py` defines a reusable letter-counting subgraph. Here we
import it, build it with the parent's own state keys (`prompt`/`reply`) via
the factory, and wire it into a small Q&A graph. A conditional edge routes
letter-counting questions to the imported subgraph and everything else to a
plain LLM `chat` node.

For counting questions the demo also asks the bare LLM directly, so you can
see it get "how many r in raspberry?" wrong while the helper gets it right.

    uv run subgraphs_reusable.py
    uv run subgraphs_reusable.py "how many s in mississippi?"
    uv run subgraphs_reusable.py "what is the capital of France?"

The "is this a counting question?" decision is delegated to the helper's
`handles()` predicate, so this file owns only the branch wiring, not the
counter's domain knowledge. A real app might use an LLM classifier instead
(see multi_agent_supervisor.py).
"""

import sys
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph

from letter_counter import make_letter_counter, handles_letter_counter

sys.stdout.reconfigure(encoding="utf-8")

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)


class ChatState(TypedDict):
    prompt: str
    reply: str


letter_counter = make_letter_counter(llm, input_key="prompt", output_key="reply")


def route(state: ChatState) -> str:
    decision = "count" if handles_letter_counter(state["prompt"]) else "chat"
    print(f"[route] -> {decision}")
    return decision


def chat(state: ChatState) -> dict:
    print("[chat] Answering with the raw LLM ...")
    response = llm.invoke([("user", state["prompt"])])
    return {"reply": response.content}


workflow = StateGraph(ChatState)

workflow.add_node("letter_counter", letter_counter)
workflow.add_node("chat", chat)

workflow.add_conditional_edges(START, route, {"count": "letter_counter", "chat": "chat"})
workflow.add_edge("letter_counter", END)
workflow.add_edge("chat", END)

graph = workflow.compile()
png_bytes = graph.get_graph(xray=1).draw_mermaid_png()
with open("subgraph_reusable.png", "wb") as f:
    f.write(png_bytes)


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else "how many r are in raspberry?"
    result = graph.invoke({"prompt": question})

    print("\n--- ANSWER ---")
    print(result["reply"])
    print("--- /ANSWER ---")


if __name__ == "__main__":
    main()
