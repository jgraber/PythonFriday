import chromadb
from chromadb.config import Settings

# create client - opt out of telemetry
client = chromadb.PersistentClient(path="demo_metadata.chroma", settings=Settings(anonymized_telemetry=False))

# create a collection
collection = client.get_or_create_collection(name="my_collection")

# add a few documents with meta data
docs = [
    # A Study in Scarlet
    "Holmes and Watson first meet, begin sharing lodgings, and Holmes applies observation and deduction to a puzzling case involving a mysterious death and a trail leading beyond London.",
    # The Sign of the Four
    "A client’s inheritance mystery leads Holmes and Watson into a hunt tied to a hidden treasure, shifting alliances, and a river pursuit that turns the investigation into an action-heavy chase.",
    # The Hound of the Baskervilles
    "A legendary curse and a threatened heir draw Holmes and Watson to the moors, where superstition clashes with rational inquiry as they track the source of seemingly supernatural danger.",
    # The Adventure of the Speckled Band
    "A terrified woman seeks Holmes’s help after her sister’s strange death; clues in a secluded estate point to a dangerous method of murder and a sinister household secret.",
    # The Final Problem
    "Holmes confronts a criminal mastermind who orchestrates crimes from the shadows, and the conflict escalates into a decisive showdown away from London.",
    # The Adventure of the Scandal in Bohemia
    "A royal client fears blackmail over a compromising photograph; Holmes faces an exceptionally clever opponent and learns that not every contest ends with a tidy victory.",
]

metadatas = [
    {
        "work_type": "novel",
        "title": "A Study in Scarlet",
        "collection": None,
        "year": 1887,
        "setting": "London",
        "themes": "origin_story|deduction|mystery",
        "characters": "Sherlock Holmes|Dr. John Watson",
        "has_holmes": True,
        "has_watson": True,
        "has_moriarty": False,
        "has_irene_adler": False,
    },
    {
        "work_type": "novel",
        "title": "The Sign of the Four",
        "collection": None,
        "year": 1890,
        "setting": "London|River Thames",
        "themes": "treasure|investigation|pursuit",
        "characters": "Sherlock Holmes|Dr. John Watson",
        "has_holmes": True,
        "has_watson": True,
        "has_moriarty": False,
        "has_irene_adler": False,
    },
    {
        "work_type": "novel",
        "title": "The Hound of the Baskervilles",
        "collection": None,
        "year": 1902,
        "setting": "Devonshire|moor",
        "themes": "superstition_vs_reason|inheritance|threat",
        "characters": "Sherlock Holmes|Dr. John Watson",
        "has_holmes": True,
        "has_watson": True,
        "has_moriarty": False,
        "has_irene_adler": False,
    },
    {
        "work_type": "short_story",
        "title": "The Adventure of the Speckled Band",
        "collection": "The Adventures of Sherlock Holmes",
        "year": 1892,
        "setting": "English countryside|estate",
        "themes": "family_secret|murder_method|investigation",
        "characters": "Sherlock Holmes|Dr. John Watson",
        "has_holmes": True,
        "has_watson": True,
        "has_moriarty": False,
        "has_irene_adler": False,
    },
    {
        "work_type": "short_story",
        "title": "The Final Problem",
        "collection": "The Memoirs of Sherlock Holmes",
        "year": 1893,
        "setting": "London|Switzerland",
        "themes": "mastermind|pursuit|showdown",
        "characters": "Sherlock Holmes|Dr. John Watson|Professor Moriarty",
        "has_holmes": True,
        "has_watson": True,
        "has_moriarty": True,
        "has_irene_adler": False,
    },
    {
        "work_type": "short_story",
        "title": "A Scandal in Bohemia",
        "collection": "The Adventures of Sherlock Holmes",
        "year": 1891,
        "setting": "London",
        "themes": "blackmail|clever_adversary|social_status",
        "characters": "Sherlock Holmes|Dr. John Watson|Irene Adler",
        "has_holmes": True,
        "has_watson": True,
        "has_moriarty": False,
        "has_irene_adler": True,
    },
]

ids = [f"holmes-canon-{i}" for i in range(len(docs))]

collection.upsert(
    ids=ids,
    documents=docs,
    metadatas=metadatas,
)

# Query for semantically similar documents
question = "criminal mastermind behind a web of crimes"
results = collection.query(
    query_texts=[question],
    n_results=5,
    where={"has_moriarty": True}
)

print(question)
for id, document, distance in zip(results["ids"][0], results["documents"][0], results["distances"][0]):
    print(f"#{id}: >{document}< with a distance of {distance}")


for i in range(len(results["ids"][0])):
    print("----")
    print(results["ids"][0][i], results["distances"][0][i])
    print(results["metadatas"][0][i]["title"])
    print(results["documents"][0][i])