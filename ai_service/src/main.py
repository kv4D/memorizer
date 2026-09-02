from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from .configs import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Memorizer AI service",
    version="0.1.0",
    description="AI service for generation, indexing and more",
    lifespan=lifespan,
)


@app.get("/")
def ping():
    return "pong"


if __name__ == "__main__":
    uvicorn.run(app, port=settings.AI_SERVICE_PORT, host=settings.AI_SERVICE_HOST)
