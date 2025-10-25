from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

# 1. Setup the search with DuckDuckGo
search = DuckDuckGoSearchAPIWrapper(max_results=5)

def fetch_duckduckgo_results(query: str):
    results = search.results(query, max_results=5)
    if not results:
        return {"snippets": "No relevant results found.", "query": query}
    
    formatted = "\n\n".join(
        [f"Title: {r['title']}\nSnippet: {r['snippet']}\nURL: {r['link']}" for r in results]
    )
    # print(formatted)
    return {"snippets": formatted, "query": query}

fetch_results = RunnableLambda(fetch_duckduckgo_results)

# 2. Define a prompt that includes the search result
prompt = PromptTemplate.from_template("""
You are an expert assistant that summarizes accurate, web-based information.

Below are 5 DuckDuckGo search results for the query:
"{query}"

{snippets}

Based on these results, write a concise, factual, and well-structured summary answer.
Include useful insights but avoid speculation or repetition.
""")

# 3. Define the LLM
llm = ChatOpenAI(
    model="mistral",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="not-needed",
    temperature=0.2
)

# 4. Create the chain
chain = fetch_results | prompt | llm

# 5. Loop for questions
while True:
    query = input("You: ")
    if query.lower() in ["quit", "exit", "end"]:
        break
    result = chain.invoke(query)
    print("\n🧾 Synthesized Answer:\n")
    print(result.content)