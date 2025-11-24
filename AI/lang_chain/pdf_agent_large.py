from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Load the PDF
loader = PyPDFLoader("pg2852.txt.pdf")
pages = loader.load()
pdf_text = "\n\n".join([page.page_content for page in pages])
print(f"Length of PDF Text: {len(pdf_text)}")


# 2. Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # max characters per chunk
    chunk_overlap=100,   # overlap to preserve context
    length_function=len, # optional, default is len
)

chunks = text_splitter.split_text(pdf_text)
print(f"Total chunks created: {len(chunks)}")


# 3. initialise the TfidfVectorizer and vectorise the chunks
vectorizer = TfidfVectorizer()
vectorizer.fit(chunks)
vectorized_chunks = vectorizer.transform(chunks)


# 4. Using the vector's tuple as the dictionary key
vector_chunk_dict = {}
for i, vec in enumerate(vectorized_chunks):
    # Convert sparse vector to dense and then tuple to make it hashable
    vec_tuple = tuple(vec.toarray()[0])
    vector_chunk_dict[vec_tuple] = chunks[i]

print(f"Dictionary contains {len(vector_chunk_dict)} vectors.")


# 5. Create the LLM
llm = ChatOpenAI(
    model="mistral",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="not-needed",
    temperature=0
)


# 6. Create a strict prompt
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant that only answers using the provided PDF context.\n"
        "If the answer is not in the context, say 'I don’t know based on this document.'\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
)


# 7. Build the new Runnable chain
chain = prompt | llm


# 8. Ask a question interactively
while True:
    user_input = input("\n\nYou: ")
    if user_input.lower() in ["quit", "exit", "end"]:
        break
    
    # a. vectorize user input
    user_vec = vectorizer.transform([user_input])
    
    # b. compute cosine similarity with all chunks
    similarities = cosine_similarity(user_vec, vectorized_chunks)[0]  # shape = (num_chunks,)
    
    # c. get top 10 matches and merge them into a single text
    top_indices = np.argsort(similarities)[::-1][:10]  # descending order
    top_chunks_text = "\n".join([chunks[idx] for idx in top_indices])
    
    # d. send the request to the LLM and print the output
    result = chain.invoke({"context": top_chunks_text, "question": user_input})
    print("Bot:", result.content)
