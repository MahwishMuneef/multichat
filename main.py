import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use the correct model name with v1 endpoint
model = genai.GenerativeModel("gemini-1.5-pro")

print("Gemini Chatbot (type 'exit' to quit)\n")

while True:
    prompt = input("You: ")
    if prompt.lower() == "exit":
        break
    try:
        response = model.generate_content(prompt)
        print("Bot:", response.text)
    except Exception as e:
        print("Error:", e)

