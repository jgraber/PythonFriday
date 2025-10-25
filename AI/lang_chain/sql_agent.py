import seaborn as sns
import pandas as pd
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent


# 1. Load Titanic dataset from seaborn and store it as CSV file
csv_path = "titanic.csv"
sns.load_dataset("titanic").to_csv(csv_path, index=False)


# 2. Read the CSV file using Pandas and store it in SQLite
df = pd.read_csv(csv_path)
db_file = "titanic.db"
conn = sqlite3.connect(db_file)
table_name = "passengers"
df.to_sql(table_name, conn, if_exists="replace", index=False)
conn.close()


# 3. Define the LLM (adjust API base/port for your local setup)
llm = ChatOpenAI(
    model="mistral",  # or "mistral:7b-instruct", etc.
    openai_api_base="http://localhost:1234/v1",  # LM Studio default
    openai_api_key="not-needed",
    temperature=0.1,
)


# 4. Create the SQL Agent
db_uri = f"sqlite:///{db_file}"
db = SQLDatabase.from_uri(db_uri)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,
    handle_parsing_errors=True,
    agent_type="tool-calling",
)


# 5. Interactive loop
print("✅ SQL Agent ready! Ask me anything about the Titanic database.")
print("Type 'exit' to quit.\n")

while True:
    query = input("🧠 Question: ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Bye!")
        break

    try:
        answer = agent_executor.invoke({"input": query})
        print(f"💬 Answer: {answer["output"]}\n")
    except Exception as e:
        print(f"⚠️ Error: {e}\n")
