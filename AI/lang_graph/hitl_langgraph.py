import os
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import uuid

# 1. Define the Tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers together."""
    return a * b

tools = [multiply]

# 2. Create the LLM
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",           
    model="openai/gpt-oss-20b",
    temperature=0.1
)

# 3. Bind tools to the model so it knows how to call them
model = llm.bind_tools(tools)

# 4. Define the State
class State(TypedDict):
    # Annotated with add_messages so history is preserved in the loop
    messages: Annotated[list[BaseMessage], add_messages]

# 5. Create the agent & tool node
def agent_node(state: State):
    """The LLM decides if it needs a tool or can answer directly."""
    print("--- AGENT: Reasoning ---")
    response = model.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 6. Define the Looping Logic
def should_continue(state: State) -> Literal["continue", "loop"]:
    """Check if the LLM requested a tool or is finished."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "loop"
    return "continue"

# 7. Build the Graph
workflow = StateGraph(State)

# Add Nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node) # Add the prebuilt node

# Define Edges
workflow.add_edge(START, "agent")

# Use the prebuilt tools node in your edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "loop": "tools",  # Matches the node name above
        "continue": END,
    }
)

workflow.add_edge("tools", "agent")


# 8. Compile with checkpointer and interrupt
memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["tools"])

# Print the visual structure
png_bytes = app.get_graph().draw_mermaid_png()
with open("tools_toolnode.png", "wb") as f:
    f.write(png_bytes)

# 9. Set a thread ID (required for checkpoints)
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

# 10. Start the initial run
initial_input = {"messages": [("user", "What is 144 multiplied by 2?")]}

print("--- Starting Graph ---")
for event in app.stream(initial_input, config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# 11. Human-in-the-loop Check
snapshot = app.get_state(config)
if snapshot.next:
    print(f"\n>>> PAUSED: The agent wants to call tools: {snapshot.next}")
    user_approval = input("Do you allow the tool execution? (yes/no): ")

    if user_approval.lower() == "yes":
        print("--- Resuming Graph ---")
        # Resume by passing None as input (it picks up from the checkpoint)
        for event in app.stream(None, config, stream_mode="values"):
            event["messages"][-1].pretty_print()
    else:
        print("Tool execution denied by user.")