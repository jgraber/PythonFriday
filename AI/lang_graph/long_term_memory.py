import json
import sys
import uuid
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore

sys.stdout.reconfigure(encoding="utf-8")

MEMORY_FILE = Path("memory.json")
DEFAULT_USER_ID = "demo-user"


def load_store() -> InMemoryStore:
    """Build a fresh InMemoryStore and rehydrate it from memory.json if present."""
    store = InMemoryStore()
    if MEMORY_FILE.exists():
        for record in json.loads(MEMORY_FILE.read_text(encoding="utf-8")):
            store.put(tuple(record["namespace"]), record["key"], record["value"])
    return store


def dump_store(store: InMemoryStore) -> None:
    """Serialize every item in the store to memory.json."""
    records = [
        {"namespace": list(ns), "key": item.key, "value": item.value}
        for ns in store.list_namespaces()
        for item in store.search(ns)
    ]
    MEMORY_FILE.write_text(json.dumps(records, indent=2), encoding="utf-8")


class State(TypedDict):
    user_id: str
    greeting: str
    known: bool


def greeter(state: State, *, store: BaseStore) -> dict:
    record = store.get(("users", state["user_id"]), "profile")
    if record is not None:
        return {
            "greeting": f"Hi {record.value['name']}, welcome back!",
            "known": True,
        }
    return {"greeting": "Hello user, what is your name?", "known": False}


store = load_store()

workflow = StateGraph(State)

workflow.add_node("greeter", greeter)

workflow.add_edge(START, "greeter")
workflow.add_edge("greeter", END)

# Use the configured memory object
graph = workflow.compile(checkpointer=InMemorySaver(), store=store)


def main() -> None:
    user_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USER_ID
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    result = graph.invoke({"user_id": user_id}, config)
    print(result["greeting"])

    if not result["known"]:
        name = input("> ").strip()
        if name:
            store.put(("users", user_id), "profile", {"name": name})
            dump_store(store)
            print(f"Nice to meet you, {name}. Run me again to see me remember.")


if __name__ == "__main__":
    main()
