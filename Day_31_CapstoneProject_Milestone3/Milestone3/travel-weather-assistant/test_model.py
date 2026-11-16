
from pathlib import Path
from llama_cpp import Llama

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "qwen2.5-3b-instruct-q4_k_m.gguf"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

print("Loading Qwen2.5-3B model...")

llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=4096,
    n_threads=4,
    verbose=False
)

print("Model loaded successfully!")

response = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful travel and weather assistant."
        },
        {
            "role": "user",
            "content": "What should I pack for a business trip to Jaipur?"
        }
    ],
    temperature=0.3,
    max_tokens=300
)

print("\nAssistant:")
print(response["choices"][0]["message"]["content"])
