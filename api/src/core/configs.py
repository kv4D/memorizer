from pydantic_settings import BaseSettings, SettingsConfigDict

# path to the env file
ENV_PATH = '.env'


class APISettings(BaseSettings):
    """API settings."""

    TITLE: str = "FastAPI"
    DESCRIPTION: str = "API for the Memorizer application"
    VERSION: str = "0.1.0"

    API_HOST: str
    API_PORT: int

    API_SECRET_KEY: str
    API_ALGORITHM: str
    API_ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_REFRESH_TOKEN_EXPIRE_MINUTES: int

    DEBUG_MODE: bool = True

    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')


class DatabaseSettings(BaseSettings):
    """Database settings."""

    DATABASE_HOST: str
    DATABASE_PORT_PRIVATE: int
    DATABASE_PORT_PUBLIC: int

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')

    def get_database_url(self) -> str:
        """Get database url."""
        url = f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT_PRIVATE}/{self.DATABASE_NAME}"
        return url


# import these settings in other modules
api_settings = APISettings()  # type: ignore
database_settings = DatabaseSettings()  # type: ignore

