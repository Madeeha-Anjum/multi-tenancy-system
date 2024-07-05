import os
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_settings():
    environment = os.getenv("ENVIRONMENT")

    if not environment:
        raise ValueError("set ENVIRONMENT to 'development' or 'production'")

    if environment == "development":
        return Settings.instance()
    else:
        raise ValueError("ENVIRONMENT variable is not set to development or production", environment)


class Settings(BaseSettings):
    SettingsConfigDict(
        env_prefix="",  # prefix for environment variables
        case_sensitive=True,
        populate_by_name=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = "development"
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    APP_NAME: str = "Multi tenancy API"

    # loaded from environment and .env file
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    _instance: ClassVar[None] = None

    def __new__(cls):
        if cls._instance is None:
            print(f"\n{__name__}=====> \033[92mSettings __new__\033[0m\n")
            cls._instance = super(Settings, cls).__new__(cls)
            # Put any initialization here.
            return cls._instance
        return cls._instance

    @classmethod
    def instance(cls) -> "Settings":
        print(f"\n{__name__}=====> \033[92mSettings instance\033[0m\n")
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
