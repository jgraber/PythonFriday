import sys
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, MessagesState, StateGraph

sys.stdout.reconfigure(encoding="utf-8")

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)


def chatbot(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


graph = (
    StateGraph(MessagesState)
    .add_node("chatbot", chatbot)
    .add_edge(START, "chatbot")
    .add_edge("chatbot", END)
    .compile(checkpointer=InMemorySaver())
)


def ask(question: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke({"messages": [{"role": "user", "content": question}]}, config)
    return result["messages"][-1].content


# Thread A: the model is told a name, then asked to recall it on the next turn.
print("Thread A, turn 1:", ask("Hi! My name is Johnny.", thread_id="A"))
print("Thread A, turn 2:", ask("What is my name?", thread_id="A"))

# Thread B: same question, fresh thread_id — checkpointer has no history, so the
# model cannot answer. This is the point: short-term memory is *thread-scoped*.
print("Thread B, turn 1:", ask("What is my name?", thread_id="B"))
