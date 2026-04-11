import random
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class State(TypedDict):
    number: int
    result_message: str

# 2. Define the Nodes
def generator_node(state: State):
    """Generates a random number between 1 and 100."""
    print("--- GENERATING Number ---")
    random_num = random.randint(1, 100)
    print(f"The random number is {random_num}")
    return {"number": random_num}

def processor_node(state: State):
    """Determines if the number is even or odd and formats the message."""
    print("--- PROCESSING Number ---")
    num = state["number"]
    parity = "even" if num % 2 == 0 else "odd"
    message = f"You entered {num}, it is {parity}."
    return {"result_message": message}

# 3. Build the Graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("generator", generator_node)
workflow.add_node("processor", processor_node)

# Connect nodes
workflow.add_edge(START, "generator")
workflow.add_edge("generator", "processor")
workflow.add_edge("processor", END)

# Compile
app = workflow.compile()
png_bytes = app.get_graph().draw_mermaid_png()
with open("pass_data.png", "wb") as f:
    f.write(png_bytes)
    
# 4. Execute
# We start with an empty dict because the generator creates the first value
final_output = app.invoke({"number": 0, "result_message": ""})

print("\n--- FINAL OUTPUT ---")
print(final_output["result_message"])