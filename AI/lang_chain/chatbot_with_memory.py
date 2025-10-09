from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 1. Define the LLM
llm = ChatOpenAI(
    model="mistral",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="not-needed",
    temperature=0.7
)

# 2. Define a prompt that includes chat history + user input
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Keep responses concise."),
    MessagesPlaceholder(variable_name="history"),   # stores past conversation
    ("human", "{input}")                            # current user message
])

# 3. Create a chain
chain = prompt | llm

# 4. Message history store (per session)
chat_histories = {}

def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]

# 5. Wrap in RunnableWithMessageHistory
chat_with_history = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",   # matches {input} in the prompt
    history_messages_key="history"
)

# 6. Simple REPL loop
session_id = "user1"

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "end"]:
        break
    response = chat_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    print("Bot:", response.content)
