
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Project paths
PROJECT_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = PROJECT_DIR / "Documents"

# 2. Read documents
documents = []

for file_path in DOCUMENT_DIR.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={"source": file_path.name}
        )
    )

# 3. Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20
)

chunks = splitter.split_documents(documents)

# 4. Load local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 5. Create ChromaDB vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="museum_langchain",
    persist_directory=str(PROJECT_DIR / "chroma_langchain")
)

print("Total chunks:", len(chunks))

# 6. Search questions
while True:
    question = input("\nEnter your question (or exit): ")

    if question.lower() == "exit":
        break

    results = vectorstore.similarity_search_with_score(
        question,
        k=2
    )

    print("\nRETRIEVED RESULTS")

    for i, (doc, distance) in enumerate(results, 1):
        print(f"\nResult {i}")
        print("Source:", doc.metadata.get("source"))
        print("Distance:", distance)
        print("Text:", doc.page_content)
