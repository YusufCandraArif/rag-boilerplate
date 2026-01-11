from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Application configuration.

    All environment variables should be defined here.
    """

    # ──────────────────────────────
    # Application
    # ──────────────────────────────
    PROJECT_NAME: str = "RAG API"
    VERSION: str = "0.1.0"
    ENV: Literal["local", "staging", "production"] = "local"

    # ──────────────────────────────
    # API
    # ──────────────────────────────
    API_PREFIX: str = "/api"

    # ──────────────────────────────
    # Vector Store (Qdrant)
    # ──────────────────────────────
    VECTOR_STORE_TYPE: Literal["qdrant"] = "qdrant"

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6334
    QDRANT_COLLECTION: str = "documents"
    QDRANT_EMBEDDING_DIM: int = 384

    # ──────────────────────────────
    # Embedding
    # ──────────────────────────────
    EMBEDDING_PROVIDER: Literal["dummy", "sentence_transformer"] = "dummy"

    # ──────────────────────────────
    # Logging
    # ──────────────────────────────
    LOG_LEVEL: str = Field("INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Safe to use across the app.
    """
    return Settings()


# Re-export for convenience
settings = get_settings()
