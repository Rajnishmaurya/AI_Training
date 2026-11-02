"""Task 2 - Split into 120-token chunks with 20-token overlap and create embeddings."""
from rag_utils import (CHUNK_OVERLAP, CHUNK_SIZE, EMBED_MODEL_NAME,
                       build_chunks, count_tokens, load_documents, load_embedding_model)

docs = load_documents()
records = build_chunks(docs)

print(f"Chunk size: {CHUNK_SIZE} tokens | Overlap: {CHUNK_OVERLAP} tokens")
print(f"Total chunks: {len(records)}")
for filename in docs:
    print(f"  {filename}: {sum(r['source'] == filename for r in records)} chunks")

print("\n--- All chunks ---")
for r in records:
    print(f"\n[{r['id']}] ({count_tokens(r['text'])} tokens)\n{r['text']}")

sample = records[0]
print("\n--- Sample chunk ---")
print(f"ID: {sample['id']} | Source: {sample['source']}\n{sample['text']}")

model = load_embedding_model()
embedding = model.encode(sample["text"])
print(f"\nEmbedding model: {EMBED_MODEL_NAME}")
print(f"Vector size: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
