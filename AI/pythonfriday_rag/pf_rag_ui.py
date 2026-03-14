import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
import chromadb

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

# --- Chainlit UI Logic ---

@cl.on_chat_start
async def start():
    # Instantiate your assistant once per session
    assistant = RAGAssistant(collection_name="posts", db_path="./PythonFridayRAG.chroma")
    chain = assistant.get_chain()
    
    # Store the chain in the user session
    cl.user_session.set("chain", chain)
    await cl.Message(content="Python Friday RAG Chatbot started. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chain from the session
    chain = cl.user_session.get("chain")
    
    # Create an empty message to stream the response into
    msg = cl.Message(content="")
    
    # Stream the response
    async for chunk in chain.astream(message.content):
        # LangChain's ChatOpenAI returns BaseMessage objects
        if hasattr(chunk, "content"):
            await msg.stream_token(chunk.content)
    
    await msg.send()