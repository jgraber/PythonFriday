from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not_needed")
prompt = "Please ask your question or 'end' to quit: "

question = input(prompt)
print("You entered: " + question)

while question.strip() != "end":
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a Python expert. Provide accurate and concise responses."
            },
            {
                "role": "user",
                "content": question,
            },        
        ],
        model="gpt-4o",
        stream=True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

    question = input(f"\n\n{prompt}")
