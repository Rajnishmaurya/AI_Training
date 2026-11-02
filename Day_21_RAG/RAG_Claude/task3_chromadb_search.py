"""Task 3 - Store chunks in a persistent ChromaDB and search the top 2 chunks."""
import sys

from rag_utils import (CHROMA_DIR, build_chunks, get_collection, load_documents,
                       load_embedding_model, print_results, search, store_chunks)

model = load_embedding_model()
collection = get_collection()

records = build_chunks(load_documents())
store_chunks(collection, model, records)
print(f"Stored {collection.count()} chunks in ChromaDB at: {CHROMA_DIR}")

# Pass a question on the command line, or use the default one
question = " ".join(sys.argv[1:]) or "How many annual leave days do employees receive?"
print_results(question, search(collection, model, question))
