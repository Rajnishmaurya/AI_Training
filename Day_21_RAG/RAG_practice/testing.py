import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from the current project directory
load_dotenv()

# Read API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Check API key
if not api_key:
    raise ValueError("OpenRouter API key not found!")

print("API key loaded successfully!")

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Test API
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in simple terms."
        }
    ]
)

print("\nAI Response:")
print(response.choices[0].message.content)