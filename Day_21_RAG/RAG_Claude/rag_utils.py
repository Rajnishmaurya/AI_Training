"""Shared helpers used by all four task scripts."""
from pathlib import Path

import tiktoken

# ---------- Settings ----------
PROJECT_DIR = Path(__file__).resolve().parent
DOCS_DIR = PROJECT_DIR / "Documents"
CHROMA_DIR = PROJECT_DIR / "chroma_db"          # persistent DB stays inside the project
COLLECTION_NAME = "cedarline_docs"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 120      # tokens per chunk
CHUNK_OVERLAP = 20    # tokens shared between neighbouring chunks
TOP_K = 2

_encoding = tiktoken.get_encoding("cl100k_base")


# ---------- Task 1: read + tokenize ----------
def load_documents() -> dict[str, str]:
    """Return {filename: text} for every .txt file in the Documents folder."""
    docs = {p.name: p.read_text(encoding="utf-8") for p in sorted(DOCS_DIR.glob("*.txt"))}
    if not docs:
        raise FileNotFoundError(f"No .txt files found in {DOCS_DIR}")
    return docs


def count_tokens(text: str) -> int:
    return len(_encoding.encode(text))


# ---------- Task 2: chunk + embed ----------
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into token windows of `chunk_size`, each overlapping the previous by `overlap`."""
    tokens = _encoding.encode(text)
    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(tokens), step):
        chunks.append(_encoding.decode(tokens[start:start + chunk_size]))
        if start + chunk_size >= len(tokens):
            break
    return chunks


def build_chunks(docs: dict[str, str]) -> list[dict]:
    """Chunk each document separately so every chunk keeps its source filename."""
    records = []
    for filename, text in docs.items():
        for i, chunk in enumerate(chunk_text(text)):
            records.append({
                "id": f"{Path(filename).stem}_chunk_{i}",
                "source": filename,
                "chunk_index": i,
                "text": chunk,
            })
    return records


def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL_NAME)


# ---------- Task 3: ChromaDB ----------
def get_collection():
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    # cosine space -> distances are cosine distances (0 = identical, larger = less similar)
    return client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})


def store_chunks(collection, model, records: list[dict]) -> None:
    embeddings = model.encode([r["text"] for r in records]).tolist()
    collection.upsert(  # upsert = safe to re-run without duplicates
        ids=[r["id"] for r in records],
        documents=[r["text"] for r in records],
        embeddings=embeddings,
        metadatas=[{"source": r["source"], "chunk_index": r["chunk_index"]} for r in records],
    )


def search(collection, model, question: str, top_k: int = TOP_K) -> list[dict]:
    query_embedding = model.encode([question]).tolist()
    res = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": doc, "source": meta["source"], "chunk_index": meta["chunk_index"], "distance": dist}
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


def print_results(question: str, results: list[dict]) -> None:
    print(f"\nQuestion: {question}")
    for rank, r in enumerate(results, start=1):
        print(f"\n  #{rank}  source={r['source']}  chunk={r['chunk_index']}  cosine distance={r['distance']:.4f}")
        print("  " + r["text"].replace("\n", "\n  "))
