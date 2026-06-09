"""EstimateAI FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1 import api_v1_router
from app.core.config import get_settings
from app.core.constants import API_V1_PREFIX
from app.core.logging import setup_logging
from app.middleware.exception_middleware import register_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    for path in (
        settings.upload_dir,
        settings.storage_original,
        settings.storage_thumbnails,
        settings.storage_previews,
        settings.storage_exports,
        settings.storage_temp,
    ):
        path.mkdir(parents=True, exist_ok=True)
    logger.info("{} started (debug={})", settings.app_name, settings.debug)
    yield
    logger.info("{} shutting down", settings.app_name)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="AI-powered construction takeoff and PDF estimation platform",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.debug else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)
    register_exception_handlers(app)

    app.include_router(api_v1_router, prefix=API_V1_PREFIX)

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        return {"status": "healthy", "app": settings.app_name}

    return app


app = create_app()
