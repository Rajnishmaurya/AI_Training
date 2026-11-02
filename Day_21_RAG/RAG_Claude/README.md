# Simple Python RAG – Cedarline Systems

## Setup (PyCharm)
1. Open this folder as a PyCharm project and create a virtual environment.
2. In the PyCharm terminal: `pip install -r requirements.txt`
3. Run > Edit Configurations > Environment variables: add `ANTHROPIC_API_KEY=your_key` (needed for Task 4 only).

## Run in order
| Script | What it shows |
|---|---|
| `task1_read_tokenize.py` | Both documents + token count per file |
| `task2_chunk_embed.py` | Chunk count, all chunks, a sample chunk, vector size (384) |
| `task3_chromadb_search.py` | Stores chunks in `chroma_db/`, prints top 2 chunks + cosine distances |
| `task4_ai_answer.py` | Retrieval + AI answer for all 5 test questions |

Tasks 3 and 4 also accept a custom question:
`python task4_ai_answer.py "How many sick days do employees get?"`

The first run downloads the all-MiniLM-L6-v2 model (~90 MB); later runs use the cache.
Keep the `chroma_db/` folder in the project for submission.
