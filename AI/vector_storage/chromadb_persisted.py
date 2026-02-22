import chromadb
from chromadb.config import Settings

# create client - opt out of telemetry
client = chromadb.PersistentClient(path="demo.chroma", settings=Settings(anonymized_telemetry=False))

# create a collection
collection = client.get_or_create_collection(name="my_collection")

# add a few documents
collection.upsert(
    documents = [
        "The cat sat on the mat.",
        "A fluffy feline lounged gracefully.",
        "The kitten played with a ball of yarn.",
        "The dog eats the bone.",
        "The car is green.",
        "The engine in the car runs on oil."
    ],
    ids=["id1", "id2", "id3","id4","id5","id6"]
)

# Query for semantically similar documents
question = "What do cats do?"
results = collection.query(
    query_texts=[question], # Chroma will embed this for you
    n_results=3 # how many results to return
)

print(question)
for i in range(len(results["ids"][0])):
    id = results["ids"][0][i]
    document = results["documents"][0][i]
    distance = results["distances"][0][i]
    
    print(f"#{id}: >{document}< with a distance of {distance}")
    

print("\n\n=====================================================\n\n")

# Query for something that is not in the data
question = "The limitations of AI"
results = collection.query(
    query_texts=[question], # Chroma will embed this for you
    n_results=10 # how many results to return
)

print(question)
for i in range(len(results["ids"][0])):
    id = results["ids"][0][i]
    document = results["documents"][0][i]
    distance = results["distances"][0][i]
    
    print(f"#{id}: >{document}< with a distance of {distance}")