import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    APP_VERSION: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    MODEL_ID: str
    MODEL_TEMPERATURE: float
    MODEL_MAX_TOKENS: int

    RETRIEVER_API_KEY: str
    RETRIEVER_TOP_K_RESULTS: int

    FHIR_CLIENT_APP_ID: str
    FHIR_CLIENT_API_BASE: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
