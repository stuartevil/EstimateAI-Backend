"""Root entry point — re-exports the FastAPI app."""

from app.main import app

__all__ = ["app"]
