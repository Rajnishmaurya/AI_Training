# EmployeeLeaveAgent: FastAPI + Redis Service

An HR assistant agent built in **Microsoft Foundry** and exposed as a service using **FastAPI**, with **Redis** for conversation/session storage. The agent answers employee leave-related questions only and refuses everything else.

## Leave Policy (defined in the agent Instructions)

| Leave Type   | Entitlement      |
|--------------|------------------|
| Casual Leave | 12 days annually |
| Sick Leave   | 10 days annually |
| Annual Leave | 18 days annually |

- Leave applications must be submitted at least **2 days in advance**, except sick leave.
- All leave requests require **manager approval**.

## Project Structure

```
.
├── main.py            # FastAPI app (POST /chat)
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (do not commit)
└── README.md
```

## Prerequisites

- Python 3.10+
- Docker Desktop (running)
- PyCharm (or any IDE)
- A Microsoft Foundry project with the `EmployeeLeaveAgent` created and deployed

## 1. Setup

```bash
# Clone / open the project in PyCharm, then create a virtual environment
python -m venv .venv

# Activate it
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configure Environment Variables

Create a `.env` file in the project root (adjust names to match your `main.py`):

```env
AZURE_AI_PROJECT_ENDPOINT=<your-foundry-project-endpoint>
AGENT_ID=<your-EmployeeLeaveAgent-id-or-name>
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

Authenticate to Azure so the app can call Foundry:

```bash
az login
```

## 3. Start Redis (Docker)

```bash
docker run -d --name employeeagnet-redis -p 127.0.0.1:6379:6379 -v employee_redis_data:/data redis:7-alpine redis-server --appendonly yes
```

What this does:
- `-d` runs the container in the background.
- `--name employeeagnet-redis` names the container.
- `-p 127.0.0.1:6379:6379` exposes Redis on localhost only.
- `-v employee_redis_data:/data` persists data in a named volume.
- `--appendonly yes` enables AOF persistence.

### Verify Redis is running

```bash
docker exec employeeagnet-redis redis-cli ping
```

Expected output:

```
PONG
```

## 4. Run the FastAPI Service

```bash
python -m uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## 5. Test the API

Open the interactive Swagger UI:

```
http://127.0.0.1:8000/docs
```

Then expand **POST /chat**, click **Try it out**, enter a message, and click **Execute**.

Or use curl (adjust the body to match your request model):

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How many casual leave days am I entitled to?"}'
```

### Sample Test Questions

| Question | Expected Behavior |
|----------|-------------------|
| How many casual leave days am I entitled to? | 12 days annually |
| Can I apply for sick leave tomorrow? | Yes, no 2-day notice needed; manager approval required |
| What is the process for applying for annual leave? | Apply 2+ days ahead, manager approval required |
| Can I take 5 days of casual leave? | Yes, within the 12-day limit, with notice and approval |
| What is the capital of France? | Refusal (out of scope) |

## 6. Useful Docker Commands

```bash
# Check running containers
docker ps

# View Redis logs
docker logs employeeagnet-redis

# Open the Redis CLI
docker exec -it employeeagnet-redis redis-cli

# Stop / start the container
docker stop employeeagnet-redis
docker start employeeagnet-redis

# Remove the container (data stays in the volume)
docker rm -f employeeagnet-redis

# Remove the data volume as well
docker volume rm employee_redis_data
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `docker: container name "/employeeagnet-redis" is already in use` | Run `docker start employeeagnet-redis`, or `docker rm -f employeeagnet-redis` and re-run the `docker run` command |
| `redis-cli ping` does not return `PONG` | Check `docker ps` and `docker logs employeeagnet-redis` |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt` |
| Authentication error calling Foundry | Run `az login` and confirm the endpoint and agent values in `.env` |
| Port 8000 already in use | Run `python -m uvicorn main:app --reload --port 8001` |