import os
import tiktoken
from sentence_transformers import SentenceTransformer


DOCUMENTS_PATH = "Documents"
encoding = tiktoken.get_encoding("cl100k_base")
documents = []

for filename in os.listdir(DOCUMENTS_PATH):
    if filename.endswith(".txt"):
        file_path = os.path.join(DOCUMENTS_PATH, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        documents.append({
            "filename": filename,
            "content": content
        })
        tokens = encoding.encode(content)
        print("\nFile:", filename)
        print("Content:\n", content)
        print("Token count:", len(tokens))


def create_chunks(text,chunk_size=120,overlap=20):
    tokens=encoding.encode(text)
    chunks=[]
    start=0
    while start<len(tokens):
        end=start+chunk_size
        chunk_tokens=tokens[start:end]
        chunk_text=encoding.decode(chunk_tokens)
        chunks.append(chunk_text) 
        start+=chunk_size-overlap
    return chunks


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
all_chunks = []
all_metadatas = []
for document in documents:
    chunks = create_chunks(document["content"])
    print("\nFile:", document["filename"])
    print("Number of chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        all_metadatas.append({
            "source": document["filename"],
            "chunk_id": i
        })
    if chunks:
        print("Sample chunk:")
        print(chunks[0])

embeddings=embedding_model.encode(all_chunks)
print("\nEmbedding vector size:", embeddings.shape[1])



import chromadb

client=chromadb.PersistentClient(path="./chroma_db")
collection=client.get_or_create_collection(name="company_documents")

collection.upsert(
    ids=[f"chunk_{i}" for i in range(len(all_chunks))],
    documents=all_chunks,
    embeddings=embeddings.tolist(),
    metadatas=all_metadatas
)

print("Chunks successfully stored in chroma db")

question = "What is the company travel allowance per day?"
question_embedding = embedding_model.encode([question])

results = collection.query(query_embeddings=question_embedding.tolist(),n_results=2,include=["documents", "metadatas", "distances"])

print("\nTOP 2 SEARCH RESULTS")

for i in range(len(results["documents"][0])):
    print("\nResult:", i + 1)
    print("Source:", results["metadatas"][0][i]["source"])
    print("Chunk:")
    print(results["documents"][0][i])
    print("Cosine distance:", results["distances"][0][i])


from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


context = "\n\n".join(results["documents"][0])

prompt = f"""
You are a company policy assistant.
Answer the question using ONLY the provided context.

If the answer is not available in the context,
say: "I cannot find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

response = ai_client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print("\nFINAL AI ANSWER:")
print(response.choices[0].message.content)


