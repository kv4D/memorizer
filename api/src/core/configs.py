from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# path to the env file
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / '.env'


class APISettings(BaseSettings):
    """API settings."""

    TITLE: str = "FastAPI"
    DESCRIPTION: str = "API for the Memorizer application"
    VERSION: str = "0.1.0"

    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    API_SECRET_KEY: str
    API_ALGORITHM: str
    API_ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_REFRESH_TOKEN_EXPIRE_MINUTES: int

    DEBUG_MODE: bool = True

    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')


print("HERE", ENV_PATH)
# import these settings in other modules
api_settings = APISettings() # type: ignore
