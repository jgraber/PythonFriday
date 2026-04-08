import random
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class State(TypedDict):
    number: int
    attempts: int
    result_message: str

# 2. Define the Nodes
def generator_node(state: State):
    """Generates a random number and increments attempt counter."""
    num = random.randint(1, 100)
    attempts = state.get("attempts", 0) + 1
    print(f"--- ATTEMPT {attempts}: Generated {num} ---")
    return {"number": num, "attempts": attempts}

def processor_node(state: State):
    """Final node reached only when an even number is found."""
    msg = f"Success! Found even number {state['number']} after {state['attempts']} attempt(s)."
    return {"result_message": msg}

# 3. Define the Looping Logic
def check_if_even(state: State) -> Literal["continue", "loop"]:
    """Check if we should proceed or try again."""
    if state["number"] % 2 == 0:
        return "continue"
    return "loop"

# 4. Build the Graph
workflow = StateGraph(State)

# Add Nodes
workflow.add_node("generator", generator_node)
workflow.add_node("processor", processor_node)

# Define Edges
workflow.add_edge(START, "generator")

# Add the Looping Conditional Edge
workflow.add_conditional_edges(
    "generator",
    check_if_even,
    {
        "continue": "processor", # Path to the next node
        "loop": "generator"      # Path back to itself
    }
)

workflow.add_edge("processor", END)

# Compile and Run
app = workflow.compile()

# Initial state
initial_state = {"number": 0, "attempts": 0, "result_message": ""}
final_output = app.invoke(initial_state)

print("\n--- FINAL RESULT ---")
print(final_output["result_message"])