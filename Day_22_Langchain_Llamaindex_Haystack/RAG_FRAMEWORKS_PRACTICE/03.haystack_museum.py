
from pathlib import Path

from haystack import Document, Pipeline

from haystack.components.preprocessors import DocumentSplitter

from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder
)

from haystack.components.writers import DocumentWriter

from haystack.document_stores.in_memory import InMemoryDocumentStore

from haystack.components.retrievers.in_memory import (
    InMemoryEmbeddingRetriever
)


# 1. Project paths
PROJECT_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = PROJECT_DIR / "Documents"

# 2. Load documents
documents = []

for file_path in DOCUMENT_DIR.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            content=text,
            meta={"source": file_path.name}
        )
    )

print("Documents loaded:", len(documents))

# 3. Create document store
document_store = InMemoryDocumentStore()

# 4. Create indexing pipeline
indexing_pipeline = Pipeline()

indexing_pipeline.add_component(
    "splitter",
    DocumentSplitter(
        split_by="word",
        split_length=100,
        split_overlap=15
    )
)

indexing_pipeline.add_component(
    "embedder",
    SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

indexing_pipeline.add_component(
    "writer",
    DocumentWriter(document_store=document_store)
)

# 5. Connect indexing components
indexing_pipeline.connect(
    "splitter.documents",
    "embedder.documents"
)

indexing_pipeline.connect(
    "embedder.documents",
    "writer.documents"
)

# 6. Run indexing
indexing_pipeline.run({
    "splitter": {
        "documents": documents
    }
})

print("Documents indexed:", document_store.count_documents())

# 7. Create query pipeline
query_pipeline = Pipeline()

query_pipeline.add_component(
    "text_embedder",
    SentenceTransformersTextEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

query_pipeline.add_component(
    "retriever",
    InMemoryEmbeddingRetriever(
        document_store=document_store,
        top_k=2
    )
)

query_pipeline.connect(
    "text_embedder.embedding",
    "retriever.query_embedding"
)

# 8. Search questions
while True:
    question = input("\nEnter your question (or exit): ")

    if question.lower() == "exit":
        break

    results = query_pipeline.run({
        "text_embedder": {
            "text": question
        }
    })

    retrieved_documents = results["retriever"]["documents"]

    print("\nRETRIEVED RESULTS")

    for i, doc in enumerate(retrieved_documents, 1):
        print(f"\nResult {i}")
        print("Source:", doc.meta.get("source", "unknown"))
        print("Score:", doc.score)
        print("Text:", doc.content)
