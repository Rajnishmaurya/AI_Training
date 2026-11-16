
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI-Powered Travel & Weather Advisory Assistant",
    description=(
        "An AI-powered assistant for employee business trips "
        "and destination weather advisories."
    ),
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Travel and Weather Advisory Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
