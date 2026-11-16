
from pathlib import Path
from huggingface_hub import hf_hub_download

# Hugging Face repository
REPO_ID = "Qwen/Qwen2.5-3B-Instruct-GGUF"

# Model filename
FILENAME = "qwen2.5-3b-instruct-q4_k_m.gguf"

# Local download directory
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

print("Starting Qwen 2.5 3B model download...")

model_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    local_dir=str(MODEL_DIR)
)

print("\nModel downloaded successfully!")
print(f"Model location: {model_path}")
