# AI-Powered Travel & Weather Advisory Assistant

A conversational AI assistant that helps employees prepare for business trips by retrieving trip information, checking destination weather forecasts, and generating practical travel recommendations.

The application uses **FastAPI, SQLite, Redis, LangChain, Qwen 2.5 3B (GGUF), and the Open-Meteo API**.

---

## 1. Project Overview

Organizations often require employees to prepare for business trips across different destinations. Employees need information about their travel schedules, destination weather, and appropriate travel essentials.

This project provides an AI-powered assistant that allows employees to:

- Register business trips.
- Retrieve previously saved trip information.
- Obtain destination weather forecasts.
- Ask travel-related questions.
- Ask follow-up questions without repeating trip details.
- Receive practical travel recommendations based on available weather information.

### Key Features

- **Trip Management:** Create and retrieve employee trips using FastAPI and SQLite.
- **Weather Integration:** Retrieve destination coordinates and weather forecasts using Open-Meteo.
- **AI-powered Advisory:** Generate travel recommendations using a locally hosted Qwen GGUF model through LangChain.
- **Conversational Memory:** Maintain session-specific conversation history and trip context using Redis.
- **Input Validation:** Validate travel dates and required information.
- **Error Handling:** Handle invalid destinations, unsupported forecast dates, and external API failures without inventing weather conditions.
- **Interactive API Documentation:** Test endpoints through Swagger UI.

---

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| AI Orchestration | LangChain |
| Local Language Model | Qwen 2.5 3B Instruct (GGUF) |
| Model Runtime | llama-cpp-python |
| Conversational Memory | Redis |
| Weather API | Open-Meteo |
| Data Validation | Pydantic |
| API Testing | Swagger UI |

---

## 3. System Architecture

The application follows a tool-based processing workflow.

### Request Processing Flow

1. An employee submits a trip-related question through the FastAPI endpoint.
2. The application identifies the employee's trip using the trip ID or previously stored Redis session context.
3. The trip retrieval tool fetches trip details from SQLite.
4. The weather retrieval tool obtains destination coordinates through Open-Meteo Geocoding and retrieves the weather forecast.
5. LangChain connects the retrieved information with the local language model to generate a travel advisory.
6. Redis stores recent conversation messages and trip context for follow-up questions.
7. FastAPI returns the response to the employee.

### Architecture Components

- **FastAPI:** Handles HTTP requests and responses.
- **SQLite:** Stores employee trip information.
- **Trip Tool:** Retrieves saved trip details.
- **Weather Tool:** Retrieves weather information from Open-Meteo.
- **LangChain:** Connects the tools and language model.
- **Qwen GGUF:** Generates natural-language travel recommendations.
- **Redis:** Maintains conversation history and session-specific trip context.

---

## 4. Project Structure

```text
travel-weather-assistant/
│
├── app/
│   ├── __init__.py
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   └── travel_assistant.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── memory_service.py
│   │   ├── trip_service.py
│   │   └── weather_service.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── trip_tools.py
│   │   └── weather_tools.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── models/
│   └── qwen2.5-3b-instruct-q4_k_m.gguf
│
├── download_model.py
├── init_database.py
│
├── test_model.py
├── test_langchain.py
├── test_trip_crud.py
├── test_trip_tools.py
├── test_weather.py
├── test_weather_tools.py
├── test_travel_assistant.py
├── test_memory.py
└── test_memory_assistant.py
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
└── trips.db
```

**Note:** The `models/` directory and `trips.db` are local runtime files and should not be committed to Git.

---

## 5. Prerequisites

Install the following before running the application:

- Python 3.10 or later.
- Git.
- Docker Desktop (for running Redis using a local container).
- Sufficient disk space and RAM for the Qwen GGUF model.

The application uses a CPU-based GGUF model configuration.

---

## 6. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd travel-weather-assistant
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

For Windows CPU-based GGUF installation, install the CPU wheel first:

```powershell
python -m pip install --only-binary=:all: llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

Then install the remaining project dependencies:

```powershell
pip install -r requirements.txt
```

Verify the installation:

```powershell
python -m pip check
```

### Step 4: Download the Language Model

The application uses the Qwen 2.5 3B Instruct GGUF model.

Model repository:

https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF

Expected model file:

```text
qwen2.5-3b-instruct-q4_k_m.gguf
```

Create the model directory if it does not exist:

```powershell
New-Item -ItemType Directory -Force models
```

Download the model using the project's download script:

```powershell
python download_model.py
```

Verify that the model exists:

```powershell
Get-ChildItem .\models
```

The expected model path is:

```text
models/qwen2.5-3b-instruct-q4_k_m.gguf
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root.

Add:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_TTL=86400
```

The `.env.example` file provides the configuration template.

Do not commit `.env` to Git.

### Step 6: Start Redis

Start Redis using Docker:

```powershell
docker run -d --name travel-redis -p 6379:6379 redis:7
```

Verify that the container is running:

```powershell
docker ps
```

Check the Redis connection:

```powershell
docker exec -it travel-redis redis-cli ping
```

Expected output:

```text
PONG
```

### Step 7: Initialize the SQLite Database

Run:

```powershell
python init_database.py
```

This initializes the SQLite database and creates the required trip table.

The database file is:

```text
trips.db
```

---

## 7. Running the Application

From the project root, execute:

```powershell
python -m uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

### Swagger UI

Open:

http://127.0.0.1:8000/docs

Swagger UI allows you to execute and test the API endpoints interactively.

### Health Check

Endpoint:

```http
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

## 8. API Endpoints

The application exposes three primary endpoints.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/trips` | Create a new employee trip |
| GET | `/trips/{trip_id}` | Retrieve trip details |
| POST | `/assistant/ask` | Ask the travel assistant |

### 8.1 Create a Trip

**Endpoint:**

```http
POST /trips
```

**Request:**

```json
{
  "employee_id": "EMP205",
  "destination": "Mumbai",
  "start_date": "2026-11-20",
  "end_date": "2026-11-22",
  "purpose": "Client meeting"
}
```

**Expected response:** `201 Created`

The response includes a generated unique trip ID.

### 8.2 Retrieve a Trip

**Endpoint:**

```http
GET /trips/{trip_id}
```

Example:

```http
GET /trips/ac4f04f8-38d0-49d0-97ac-869557f3670b
```

The API retrieves the corresponding trip information from SQLite.

If the trip does not exist, the API returns `404 Not Found`.

### 8.3 Ask the Travel Assistant

**Endpoint:**

```http
POST /assistant/ask
```

**Request:**

```json
{
  "session_id": "employee-EMP205-session",
  "trip_id": "YOUR_GENERATED_TRIP_ID",
  "question": "What weather should I expect during my trip?"
}
```

The assistant retrieves the saved trip, obtains weather information, and generates a travel advisory.

### 8.4 Follow-up Question

Use the same session ID without providing the trip ID again.

```json
{
  "session_id": "employee-EMP205-session",
  "question": "Will I need an umbrella there?"
}
```

Redis retrieves the stored trip context and conversation history so that the assistant can understand the follow-up question.

---

## 9. Weather Integration

The project uses Open-Meteo APIs.

### Geocoding API

Resolves destination names into geographical coordinates.

```text
https://geocoding-api.open-meteo.com/v1/search
```

### Forecast API

Retrieves weather information using geographical coordinates.

```text
https://api.open-meteo.com/v1/forecast
```

### Weather Information

The application retrieves available forecast information, including:

- Maximum temperature.
- Minimum temperature.
- Precipitation probability.
- Precipitation sum.
- Weather condition descriptions.

**Forecast limitation:** Open-Meteo forecast availability is date-dependent. The application validates the requested dates against its configured forecast range. Unsupported dates and API failures are reported without inventing weather information.

---

## 10. Redis Conversational Memory

Redis maintains conversation context using a session ID.

The application stores:

- Recent user messages.
- Assistant responses.
- The trip ID associated with a session.

The implementation uses separate Redis keys for conversation history and trip context.

### Example Interaction

First question:

```text
What weather should I expect for my Mumbai trip?
```

Follow-up:

```text
Will I need an umbrella there?
```

The assistant uses the stored session context to identify Mumbai without requiring the employee to repeat the destination.

Session data has a configurable expiration time, controlled by:

```env
REDIS_TTL=86400
```

This corresponds to 24 hours.

---

## 11. Testing

The project includes individual test scripts for its main components.

Run the tests from the project root.

| Test File | Purpose |
|---|---|
| `test_model.py` | Verify local GGUF model loading |
| `test_langchain.py` | Verify LangChain model integration |
| `test_trip_crud.py` | Test trip creation and retrieval |
| `test_trip_tools.py` | Test the trip retrieval tool |
| `test_weather.py` | Test Open-Meteo weather integration |
| `test_weather_tools.py` | Test the weather tool |
| `test_travel_assistant.py` | Test assistant orchestration |
| `test_memory.py` | Test Redis memory operations |
| `test_memory_assistant.py` | Test follow-up conversation context |

Example:

```powershell
python test_memory_assistant.py
```

### Required Validation Scenarios

The application should be tested for:

1. Creating a new employee trip.
2. Retrieving an existing trip.
3. Asking for destination weather.
4. Asking a follow-up question using the same session.
5. Rejecting invalid travel dates.
6. Handling missing destinations.
7. Handling unavailable weather forecasts and external API failures.

---

## 12. Error Handling

The application is designed to handle common failure scenarios.

| Scenario | Expected Behavior |
|---|---|
| Invalid travel dates | Reject the request through input validation |
| Nonexistent trip ID | Return a trip-not-found response |
| Invalid destination | Report that the destination could not be resolved |
| Unsupported forecast dates | Clearly explain that the forecast is unavailable |
| Weather API failure | Return an unavailable-weather response |
| Missing Redis session context | Ask the employee to provide a trip ID |

The assistant must not fabricate weather information when the external weather service cannot provide a forecast.

---

## 13. Git and Large Model Files

The project uses `.gitignore` to prevent local runtime files from being committed.

Ignored files include:

- `.venv/`
- `.env`
- `models/`
- `*.gguf`
- `trips.db`

The model must be downloaded locally using the provided model download script.

The `.env.example`, Python source code, `requirements.txt`, and README should be included in the repository.


## 14. References

- Open-Meteo: https://open-meteo.com/
- Open-Meteo Geocoding API: https://open-meteo.com/en/docs/geocoding-api
- Open-Meteo Forecast API: https://open-meteo.com/en/docs
- LangChain Documentation: https://python.langchain.com/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Redis Documentation: https://redis.io/docs/
- Qwen 2.5 GGUF Model: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF

---

## 15. Project Status

The application has been implemented and tested for its core workflows:

- FastAPI application and health check.
- Trip creation and retrieval.
- SQLite persistence.
- Open-Meteo forecast retrieval.
- LangChain-based assistant responses.
- Redis-backed conversation history and trip context.
- Follow-up questions using session memory.
- Invalid travel-date validation.

**Implementation note:** The current implementation runs Qwen GGUF directly through `llama-cpp-python` and LangChain's `ChatLlamaCpp` integration. The assessment specification names Ollama as the required local model runtime. This implementation therefore needs an Ollama integration or an approved alternative to claim strict compliance with that requirement.
