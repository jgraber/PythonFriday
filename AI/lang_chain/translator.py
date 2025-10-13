from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# 1. Define the LLM
llm = ChatOpenAI(
    model="not-needed",  # LM Studio ignores this
    openai_api_base = "http://localhost:1234/v1",
    api_key = "not-needed",  # LM Studio ignores this
    temperature = 0.3,
)

# 2. Create the prompt
prompt = ChatPromptTemplate.from_template(
    "Translate the following English text into French:\n\n{text}"
)

# 3. Create a chain
chain = prompt | llm | StrOutputParser()

# 4. Run the translator
if __name__ == "__main__":
    text = input("Enter English text: ")
    french = chain.invoke({"text": text})
    print("\n🇫🇷 Translation:\n", french)
