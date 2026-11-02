"""Task 4 - Retrieve context from ChromaDB and get a grounded answer from a free AI model.

Uses OpenRouter's OpenAI-compatible API with the "openrouter/free" model, which picks an
available free model automatically. Requires OPENROUTER_API_KEY in a .env file
(project folder or a parent folder) or as an environment variable.
Run task3_chromadb_search.py first so the database is populated.
"""
import os
import sys

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from rag_utils import get_collection, load_embedding_model, print_results, search

MODEL = "openrouter/free"   # OpenRouter chooses an available free model for each request
NOT_FOUND = "I cannot find the answer in the provided documents."

SYSTEM_PROMPT = (
    "You answer questions about company documents. Use ONLY the information in the "
    "provided context. Do not use outside knowledge or make assumptions. "
    f'If the context does not contain the answer, reply exactly: "{NOT_FOUND}" '
    "Keep answers short and mention the source file."
)

TEST_QUESTIONS = [
    "How many annual leave days do employees receive?",
    "Which days must employees work from the office?",
    "How quickly should a lost company laptop be reported?",
    "How quickly are Priority 1 incidents acknowledged?",
    "What is the company travel allowance per day?",
]


def ask_ai(client, question: str, chunks: list[dict]) -> tuple[str, str]:
    """Send the question plus retrieved chunks to the model; return (answer, model used)."""
    context = "\n\n".join(f"[Source: {c['source']}]\n{c['text']}" for c in chunks)
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,  # some free models reason before answering, so allow room
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    answer = (response.choices[0].message.content or "").strip()
    return answer, response.model  # response.model shows which free model actually answered


def main():
    # Load OPENROUTER_API_KEY from the nearest .env file (this folder, then parent folders)
    load_dotenv(find_dotenv())
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("OPENROUTER_API_KEY not found. Add it to a .env file in the project folder "
                 "or set it as an environment variable.")

    collection = get_collection()
    if collection.count() == 0:
        sys.exit("ChromaDB is empty. Run task3_chromadb_search.py first.")

    model = load_embedding_model()
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    # Pass a question on the command line, or run all five test questions
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else TEST_QUESTIONS
    for question in questions:
        chunks = search(collection, model, question)
        print("=" * 70)
        print_results(question, chunks)
        answer, used_model = ask_ai(client, question, chunks)
        print(f"\nAI ANSWER ({used_model}): {answer}\n")


if __name__ == "__main__":
    main()