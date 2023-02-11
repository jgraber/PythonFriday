import networkx as nx
# pip install networkx

G = nx.DiGraph()
G.add_edge("B","A")
G.add_edge("C","A")
G.add_edge("D","B")
G.add_edge("D","C")
G.add_edge("E","A")
G.add_edge("E","C")
G.add_edge("E","D")

print("-" * 50)
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print("-" * 50)

for x in (node for node, out_degree in G.out_degree() if out_degree == 0):
    print(x)


G.remove_node("A")


print("-" * 50)
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print("-" * 50)


for x in (node for node, out_degree in G.out_degree() if out_degree == 0):
    print(x)


G.remove_nodes_from(["B", "C"])

print("-" * 50)
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print("-" * 50)