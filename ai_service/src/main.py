from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from .configs import service_settings
from .message_broker import message_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not message_broker.is_worker_process:
        await message_broker.startup()
    yield
    if not message_broker.is_worker_process:
        await message_broker.shutdown()


app = FastAPI(
    title="Memorizer AI service",
    version="0.1.0",
    description="AI service for generation, indexing and more",
    lifespan=lifespan,
)


@app.get("/")
async def ping():
    from .tasks import test_task
    task = await test_task.kiq()
    # Wait for the result.
    result = await task.wait_result()
    return result


if __name__ == "__main__":
    uvicorn.run(
        app,
        port=service_settings.AI_SERVICE_PORT,
        host=service_settings.AI_SERVICE_HOST,
    )
