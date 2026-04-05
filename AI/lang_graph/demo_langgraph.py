# uv pip install langgraph langchain_openai
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# 1. define a global state
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. define LLM
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",           
    model="openai/gpt-oss-20b",
    temperature=0.1
)

# 3. define a node
def call_llm(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 4. build the graph
builder = StateGraph(State)
builder.add_node("llm", call_llm)
builder.add_edge(START, "llm")
builder.add_edge("llm", END)

# 5. compile the graph and use it
graph = builder.compile()
result = graph.invoke({
    "messages": [HumanMessage(content="What is the capital city of Switzerland?")]
})
print(result["messages"][-1].content)
# Output: The capital city of Switzerland is **Bern**.