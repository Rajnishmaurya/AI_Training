
from pathlib import Path

from langchain_community.chat_models import ChatLlamaCpp


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Downloaded GGUF model
MODEL_PATH = (
    BASE_DIR
    / "models"
    / "qwen2.5-3b-instruct-q4_k_m.gguf"
)


def get_llm():
    """
    Initialize and return the local Qwen LLM.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at: {MODEL_PATH}"
        )

    llm = ChatLlamaCpp(
        model_path=str(MODEL_PATH),

        # Generation configuration
        temperature=0.2,
        max_tokens=512,

        # Context configuration
        n_ctx=4096,

        # CPU configuration
        n_threads=4,
        n_gpu_layers=0,

        verbose=False
    )

    return llm
