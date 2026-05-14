"""Resume a failed LangGraph workflow.

The first run intentionally crashes inside `fetch_metric`. The graph state up
through `research` is durable in the SQLite checkpointer, so the second run
picks up at `fetch_metric` and finishes — without re-calling the LLM in
`research`.

    uv run resume_failed.py reset      # delete resume_demo.sqlite
    uv run resume_failed.py start      # crashes mid-graph (by design)
    uv run resume_failed.py inspect    # print saved checkpoint + history
    uv run resume_failed.py resume     # picks up where the crash left off
"""

import sqlite3
import sys
from pathlib import Path
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph

sys.stdout.reconfigure(encoding="utf-8")

DB_FILE = "resume_demo.sqlite"
THREAD_ID = "resume-demo"
TOPIC = "the productivity benefits of standing desks"

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)


class State(TypedDict):
    topic: str
    research: str
    metric: str
    summary: str


def research(state: State) -> dict:
    print(f"[research] Calling LLM about: {state['topic']}")
    response = llm.invoke([
        ("user", f"In two sentences, give a research-style note about {state['topic']}."),
    ])
    return {"research": response.content}


def fetch_metric(state: State) -> dict:
    print("[fetch_metric] Calling external metrics API ...")
    if SIMULATE_CRASH:
        raise RuntimeError("Network error: timeout calling metrics API.")
    return {"metric": "Standing desks: ~12% calorie burn increase (made-up number)"}


def summarize(state: State) -> dict:
    print("[summarize] Calling LLM with research + metric ...")
    response = llm.invoke([
        ("user",
         f"Combine these into a short paragraph for a blog post:\n\n"
         f"Research: {state['research']}\n"
         f"Metric: {state['metric']}"),
    ])
    return {"summary": response.content}


arg = sys.argv[1] if len(sys.argv) > 1 else None

if arg not in {"start", "resume", "reset", "inspect"}:
    print(__doc__)
    sys.exit(1)

if arg == "reset":
    Path(DB_FILE).unlink(missing_ok=True)
    print(f"Deleted {DB_FILE}.")
    sys.exit(0)

SIMULATE_CRASH = arg == "start"

conn = sqlite3.connect(DB_FILE, check_same_thread=False)
checkpointer = SqliteSaver(conn)

workflow = StateGraph(State)

workflow.add_node("research", research)
workflow.add_node("fetch_metric", fetch_metric)
workflow.add_node("summarize", summarize)

workflow.add_edge(START, "research")
workflow.add_edge("research", "fetch_metric")
workflow.add_edge("fetch_metric", "summarize")
workflow.add_edge("summarize", END)

graph = workflow.compile(checkpointer=checkpointer)


def main() -> None:
    config = {"configurable": {"thread_id": THREAD_ID}}

    if arg == "inspect":
        state = graph.get_state(config)
        print("--- CURRENT STATE ---")
        print(f"checkpoint_id: {state.config['configurable'].get('checkpoint_id')}")
        print(f"next (pending): {state.next}")
        print(f"values: {state.values}")

        print("\n--- HISTORY (newest first) ---")
        for i, snap in enumerate(graph.get_state_history(config)):
            source = snap.metadata.get("source") if snap.metadata else None
            print(f"[{i}] next={snap.next}  source={source}  values keys={list(snap.values.keys())}")
        return

    if arg == "start":
        try:
            graph.invoke({"topic": TOPIC}, config)
        except Exception as e:
            print("*" * 60)
            print(f"ERROR: {e}")
            print("*" * 60)
        return

    print("Resuming from saved checkpoint at fetch_metric ...")
    result = graph.invoke(None, config)
    print("\n--- SUMMARY ---")
    print(result["summary"])
    print("--- /SUMMARY ---")


if __name__ == "__main__":
    main()
