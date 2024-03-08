import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    # Loaded from environment
    ENVIRONMENT: str


class Dev(BaseSettings):
    # loaded from environment and .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=True,
        populate_by_name=True,
    )
    ENVIRONMENT: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


def get_settings():
    environment = os.getenv("ENVIRONMENT")
    if environment is None:
        os.environ["ENVIRONMENT"] = "development"
        environment = os.getenv("ENVIRONMENT")

        raise ValueError("ENVIRONMENT environment variable is not set")

    if environment == "development":
        return Dev()
    else:
        return Settings()
