from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 1. Load the PDF
loader = PyPDFLoader("pf178.pdf")
pages = loader.load()
pdf_text = "\n\n".join([page.page_content for page in pages])
print(f"Length of PDF Text: {len(pdf_text)}")

# 2. Create the LLM
llm = ChatOpenAI(
    model="mistral",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="not-needed",
    temperature=0
)

# 3. Create a strict prompt
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant that only answers using the provided PDF context.\n"
        "If the answer is not in the context, say 'I don’t know based on this document.'\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
)

# 4. Build the new Runnable chain
chain = prompt | llm

# 5. Ask a question interactively
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "end"]:
        break

    result = chain.invoke({"context": pdf_text, "question": user_input})
    print("Bot:", result.content)
