"""Task 1 - Read the documents and show the token count of each file."""
from rag_utils import load_documents, count_tokens

docs = load_documents()

for filename, text in docs.items():
    print("=" * 70)
    print(f"FILE: {filename}")
    print("=" * 70)
    print(text)
    print(f"\n>>> Token count (tiktoken, cl100k_base): {count_tokens(text)}\n")
