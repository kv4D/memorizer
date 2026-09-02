from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = ".env"


class Settings(BaseSettings):
    AI_SERVICE_PORT: int
    AI_SERVICE_HOST: str

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )


# import this
settings = Settings()  # type: ignore
