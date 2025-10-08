from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not_needed")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a Python expert. Provide accurate and concise responses."
            #"content": "You provide accurate, expert-level Python guidance."
        },
        {
            "role": "user",
            "content": "What is the Zen of Python?",
        },        
    ],
    model="gpt-4o",
)
print(chat_completion.choices[0].message.content)
print(f"Model: {chat_completion.model}")

