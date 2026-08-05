from fastapi import FastAPI
import uvicorn

from src.users.api import users_router
from src.core.configs import api_settings


app = FastAPI(
    title=api_settings.TITLE,
    version=api_settings.VERSION,
    description=api_settings.DESCRIPTION
)

# add routers here
app.include_router(users_router)

def main() -> None:
    """The main function to run the FastAPI application."""
    uvicorn.run(
        "main:app",
        host=api_settings.API_HOST,
        port=api_settings.API_PORT,
        reload=api_settings.DEBUG_MODE
    )


if __name__ == "__main__":
    main()
