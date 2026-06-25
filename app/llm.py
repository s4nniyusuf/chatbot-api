from groq import Groq
from app.config import API_KEY

client = Groq(api_key=API_KEY)

def chat_with_llm(messages: list):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    print("LLM Response:", response.choices[0].message.content)
    return response.choices[0].message.content
