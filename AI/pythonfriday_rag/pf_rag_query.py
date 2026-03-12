#  uv pip install chromadb langchain_openai langchain 

import chromadb
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

class RAGAssistant:
    def __init__(self, collection_name, db_path, model_name="openai/gpt-oss-20b"):
        # Initialize database internally
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection(name=collection_name)
        
        # Initialize LLM internally
        self.llm = ChatOpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",
            model=model_name,
            temperature=0.1
        )

    def _format_prompt(self, question):
        """Internal method to query Chroma and build the string."""
        results = self.collection.query(query_texts=[question], n_results=5)
        
        context_string = ""
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            ref = meta.get("Reference", "Unknown")
            context_string += f"DOCUMENT ID: {i}\nREFERENCE LABEL: {ref}\nCONTENT: {doc}\n---\n"

        return f"""### Instruction
# Answer the user's question using ONLY the provided data in the "Context" section.

# ### Constraints
# 1. NO INLINE CITATIONS: Do not mention the source, reference title, or document ID within the body of your answer. Write the answer as a seamless narrative.
# 2. STRICT GROUNDING: Use only the provided Context. If the answer is missing, say "I do not have enough information in the provided context."
# 3. UNIQUE REFERENCES: At the very end of your response, provide a section titled "References:".
# 4. DEDUPLICATION: In the "References:" section, list every unique REFERENCE LABEL that contributed to your answer. Even if multiple context blocks have the same label, list it only once.
#    - Format: " - {{reference}}"

# ### Context
# {context_string}

# ### User Question
# {question}

# ### Answer
"""

    def handle_query(self, user_input):
        """This matches the signature LangChain expects."""
        full_prompt = self._format_prompt(user_input)
        return [HumanMessage(content=full_prompt)]

    def get_chain(self):
        """Builds the chain using the instance method."""
        return RunnableLambda(self.handle_query) | self.llm

# --- Execution ---

# 1. Instantiate the assistant (No globals!)
assistant = RAGAssistant(
    collection_name="posts", 
    db_path="./PythonFridayRAG.chroma"
)

# 2. Get the chain
chain = assistant.get_chain()

# 3. Loop
print("--- Python Friday RAG Chatbot Started (Type 'exit' to stop) ---")
while True:
    user_query = input("\nYou: ")

    if user_query.lower() in ["quit", "exit", "end"]:
        print("Goodbye!")
        break
    
    try:
        result = chain.invoke(user_query)
        
        print("\n🧾 Answer:\n")
        print(result.content)
        print("\n" + "-"*30)
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")