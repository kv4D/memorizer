from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from src.users.api import users_router
from src.memoryspaces.api import memoryspaces_router
from src.storage.api import storage_router
from src.core.configs import api_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    # startup events
    # create file statuses
    yield
    # shutdown events


app = FastAPI(
    title=api_settings.TITLE,
    version=api_settings.VERSION,
    description=api_settings.DESCRIPTION,
    lifespan=lifespan,
)

# add routers here
app.include_router(users_router)
app.include_router(memoryspaces_router)
app.include_router(storage_router)


@app.get("/")
async def ping():
    return "pong"


def main() -> None:
    """The main function to run the FastAPI application."""
    uvicorn.run(
        "main:app",
        host=api_settings.API_HOST,
        port=api_settings.API_PORT,
        reload=api_settings.DEBUG_MODE,
    )


if __name__ == "__main__":
    main()
