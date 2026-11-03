# RAG Lab – React UI for comparing free models (Lesson 11)

A browser dashboard for your RAG project, modelled on the "RAG Playground & Model Benchmark" design. You can:

- **Playground:** ask one question to up to 5 free models at once and compare answers and response times side by side. You can also mark each answer Correct or Incorrect and open the retrieved source chunks.
- **Run benchmark:** ask every model the 5 test questions, then compare accuracy, source citations, average response time and errors in a table and charts.
- **Benchmark page:** see a full question-by-model grid with every answer.
- **Logs:** review every answer saved to `rag_ui_log.csv`, with timing, auto-check and feedback.

## How it fits together

```
Browser (React, port 5173)  ->  11_rag_ui_server.py (FastAPI, port 8000)  ->  rag_core.search_chunks (ChromaDB)
                                                                           ->  OpenRouter free models
```

React can't run ChromaDB or the embedding model in the browser, so the Python server does retrieval and calls the models. It reuses your existing `rag_core.py` and `.env`.

## Files to add to your project

Copy these into the same folder as `rag_core.py` and `10_log_ai_feedback.py`:

```
Simple_Python_RAG_PyCharm/
├── rag_core.py                 (already there)
├── .env                        (already there)
├── 11_rag_ui_server.py         NEW – API server
├── rag-lab-ui/                 NEW – React app
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/ (App.jsx, Playground.jsx, BenchmarkSummary.jsx, BenchmarkPage.jsx,
│             LogsPage.jsx, ModelPicker.jsx, api.js, utils.js, styles.css, main.jsx)
├── benchmark_questions.json    created automatically on first run (edit it for your document)
└── rag_ui_log.csv              created automatically when you ask a question
```

## Requirements

- **Python packages** (in your `.venv`):
  ```powershell
  python -m pip install fastapi uvicorn openai python-dotenv
  ```
- **Node.js 18 or newer** for the React app. Download the LTS version from https://nodejs.org and check it:
  ```powershell
  node --version
  npm --version
  ```
- **`.env`** pointing at OpenRouter (the same file lesson 10 uses):
  ```dotenv
  OPENAI_API_KEY=sk-or-v1-your-key
  OPENAI_BASE_URL=https://openrouter.ai/api/v1
  # Optional: choose the 5 starting models (comma-separated)
  # UI_MODELS=nvidia/nemotron-3.5-lightning:free,qwen/qwen3.8-27b:free
  ```

## Run it (two terminals)

**Terminal 1 – Python server** (in the project folder, with `.venv` active):
```powershell
.venv\Scripts\Activate.ps1
python .\11_rag_ui_server.py
```
Leave it running. It prints `RAG Lab API running on http://127.0.0.1:8000`.

**Terminal 2 – React app** (in PyCharm, click **+** in the Terminal window to open a second tab):
```powershell
cd rag-lab-ui
npm install        # first time only
npm run dev
```
Open **http://localhost:5173** in your browser.

### Optional: one command after building
```powershell
cd rag-lab-ui
npm run build
cd ..
python .\11_rag_ui_server.py
```
The server now also serves the finished UI at **http://127.0.0.1:8000**, so you don't need the second terminal.

## Choosing models

On start-up the server picks 5 models that are free on OpenRouter right now. Use **Change models** to search the live list of free models and choose up to 5. Untick a model card to leave it out of a question or benchmark without removing it.

Free models change often. If a model card shows one of these errors, swap it out:

| Error | Meaning |
|---|---|
| 401 | API key missing or wrong in `.env` |
| 403 | Model can't be used from your own code |
| 404 | Model is no longer free |
| 429 | Model is busy; the server retries once, then wait a minute |

## Benchmark questions

`benchmark_questions.json` holds the test questions and the facts each answer must contain:

```json
[
  { "question": "How many annual leave days do employees receive?", "must_include": ["16"] },
  { "question": "Which days must employees work from the office?", "must_include": ["tuesday", "thursday"] },
  { "question": "How quickly should a lost company laptop be reported?", "must_include": ["one hour|1 hour"] }
]
```

Every item in `must_include` must appear in the answer (case doesn't matter). Use `|` for alternatives, so `"one hour|1 hour"` accepts either. **Edit this file to match your own document**, then restart the server.

## What the benchmark numbers mean

| Column | How it's measured |
|---|---|
| Accuracy | Share of answers containing all the expected facts. Failed requests count as wrong. |
| Cites sources | Share of answers that mention a retrieved chunk ID, as the prompt asks. |
| Avg. time | Average time the model took to answer, excluding failed requests. |
| Errors | Requests that failed, such as rate limits. |

The auto-check is a simple text match. Use the Correct and Incorrect buttons for your own judgement; both are saved in `rag_ui_log.csv`.

## Troubleshooting

| Problem | Fix |
|---|---|
| Page shows "Can't reach the Python server" | Start `python .\11_rag_ui_server.py` in another terminal and keep it running. |
| `npm` is not recognised | Install Node.js LTS, then close and reopen PyCharm. |
| `ModuleNotFoundError: fastapi` or `uvicorn` | Activate `.venv`, then `python -m pip install fastapi uvicorn`. |
| `Add OPENAI_API_KEY ... to the .env file` | The server reads `.env` next to `rag_core.py`. Check the key is there. |
| Change models list doesn't load | The server can't reach openrouter.ai. Check your internet connection or proxy. |
| Port 8000 already in use | Stop the other program, or change `port=8000` at the bottom of the server file and in `rag-lab-ui/vite.config.js`. |
