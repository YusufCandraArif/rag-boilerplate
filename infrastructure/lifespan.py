from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from core.config import settings
from services.embedding import EmbeddingService
from services.vector_store.qdrant_store import QdrantVectorStore
from workflows.graph import build_workflow


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    All infrastructure setup & teardown lives here.
    """

    logger.info("Starting application...")

    # ──────────────────────────────
    # Embedding service
    # ──────────────────────────────
    embedding_service = EmbeddingService(
        provider=settings.EMBEDDING_PROVIDER,
        embedding_dim=settings.QDRANT_EMBEDDING_DIM,
    )

    # ──────────────────────────────
    # Vector store
    # ──────────────────────────────
    vector_store = QdrantVectorStore(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        collection_name=settings.QDRANT_COLLECTION,
        embedding_dim=settings.QDRANT_EMBEDDING_DIM,
    )

    vector_store.ensure_collection()

    # ──────────────────────────────
    # Workflow
    # ──────────────────────────────
    workflow = build_workflow(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    # ──────────────────────────────
    # Attach to app state
    # ──────────────────────────────
    app.state.embedding_service = embedding_service
    app.state.vector_store = vector_store
    app.state.workflow = workflow

    logger.info("Application startup complete")

    yield

    # ──────────────────────────────
    # Shutdown
    # ──────────────────────────────
    logger.info("Shutting down application...")

    # If later you add close() methods:
    # await vector_store.close()

    logger.info("Application shutdown complete")
