import pandas as pd
import seaborn as sns
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI

# 1. Load Titanic data set from seaborn and store it as CSV file
csv_path = "titanic.csv"
sns.load_dataset("titanic").to_csv(csv_path, index=False)

# 2. Define the LLM
llm = ChatOpenAI(
    model="mistral",
    openai_api_base="http://host.docker.internal:1234/v1",
    openai_api_key="not-needed",
    temperature=0.1
)

# 3. Create CSV agent
agent = create_csv_agent(
    llm,
    csv_path,
    verbose=False,
    allow_dangerous_code=True
)

# 4. Loop for questions
print("✅ CSV Agent ready! Ask me anything about the Titanic dataset.")
print("Type 'exit' to quit.\n")

while True:
    query = input("🧠 Question: ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Bye!")
        break
    try:
        answer = agent.invoke(query)
        print(f"💬 Answer: {answer["output"]}\n")
    except Exception as e:
        print(f"⚠️ Error: {e}\n")
