
from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings
)

from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.vector_stores.chroma import ChromaVectorStore

import chromadb


# 1. Project paths
PROJECT_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = PROJECT_DIR / "Documents"

# 2. Load documents
documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENT_DIR)
).load_data()

print("Documents loaded:", len(documents))

# 3. Configure local embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Configure chunking
Settings.node_parser = SentenceSplitter(
    chunk_size=150,
    chunk_overlap=20
)

# 5. Create separate ChromaDB collection
client = chromadb.PersistentClient(
    path=str(PROJECT_DIR / "chroma_llamaindex")
)

collection = client.get_or_create_collection(
    "museum_llamaindex"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

# 6. Build vector index
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store
)

print("Vector index created successfully!")

# 7. Create retriever
retriever = index.as_retriever(
    similarity_top_k=2
)

# 8. Search questions
while True:
    question = input("\nEnter your question (or exit): ")

    if question.lower() == "exit":
        break

    results = retriever.retrieve(question)

    print("\nRETRIEVED RESULTS")

    for i, node in enumerate(results, 1):
        print(f"\nResult {i}")

        print(
            "Source:",
            node.metadata.get("file_name", "unknown")
        )

        print("Score:", node.score)
        print("Text:", node.text)
