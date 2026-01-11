from fastapi import FastAPI

from core.config import settings
from core.logging import setup_logging
from infrastructure.lifespan import lifespan
from api.routes import router as api_router


def create_app() -> FastAPI:
    """
    Application bootstrap.
    No business logic is allowed here.
    """
    setup_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )

    # HTTP routes
    app.include_router(api_router)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.PROJECT_NAME,
            "version": settings.VERSION,
        }

    return app


app = create_app()
