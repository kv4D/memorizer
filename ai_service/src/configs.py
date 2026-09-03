from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = ".env"


class ServiceSettings(BaseSettings):
    AI_SERVICE_PORT: int
    AI_SERVICE_HOST: str
    
    MESSAGE_BROKER_URL: str
    RESULT_BACKEND_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )


# import this
service_settings = ServiceSettings()  # type: ignore
