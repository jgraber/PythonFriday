import chromadb
from chromadb.config import Settings

telemetry_off = Settings(anonymized_telemetry=False)
client = chromadb.PersistentClient(path="PythonFridayRAG.chroma", settings=telemetry_off)

# create a collection
collection = client.get_or_create_collection(name="posts")

while True:
    user_input = input("----\n\nQuestion: ")
    if user_input.lower() in ["quit", "exit", "end"]:
        break

    results = collection.query(
        query_texts=[user_input],
        n_results=5
    )
    
    for i in range(len(results["ids"][0])):
        print("----")
        print(f'[{results["ids"][0][i]}] - distance: {results["distances"][0][i]}')
        print(results["metadatas"][0][i]["Reference"])
        print(results["documents"][0][i][:200])