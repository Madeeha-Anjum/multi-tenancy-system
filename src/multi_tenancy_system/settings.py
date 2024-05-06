# TODO create a Singleton of the settings class then get tenant singleton


import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()  # take environment variables from .env.

__all__ = ["get_settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    # Loaded from environment
    ENVIRONMENT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=True,
        populate_by_name=True,
    )


class Dev(BaseSettings):
    # loaded from environment and .env file
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    ENVIRONMENT: str
    APP_NAME: str = "Multi tenancy API"
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=True,
        populate_by_name=True,
    )


settings = Settings()


def get_settings():
    environment = settings.ENVIRONMENT
    if not environment:
        raise ValueError("ENVIRONMENT environment variable is not set")

    if environment == "development":
        return Dev()
