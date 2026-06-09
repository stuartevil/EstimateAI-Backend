"""
EstimateAI FastAPI application entry point.

Wires together routers, middleware, exception handlers, and lifecycle events.
Follows Clean Architecture: main.py is the composition root (outermost layer).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.modules.auth.router import router as auth_router
from app.modules.markups.router import router as markups_router
from app.modules.measurements.router import router as measurements_router
from app.modules.pdf.router import router as pdf_router
from app.modules.projects.router import router as projects_router
from app.modules.users.router import router as users_router
from app.shared.constants import API_V1_PREFIX
from app.shared.exceptions import (
    BadRequestError,
    ConflictError,
    EstimateAIException,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from app.shared.response import error_response

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    setup_logging()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    logger.info("{} started (debug={})", settings.app_name, settings.debug)
    yield
    logger.info("{} shutting down", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="AI-powered construction takeoff and PDF estimation platform",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# CORS — configure origins per deployment environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global exception handlers ---
# Map domain exceptions to HTTP status codes with standard response envelope


@app.exception_handler(NotFoundError)
async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response(exc.message, exc.details),
    )


@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(_request: Request, exc: UnauthorizedError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=error_response(exc.message, exc.details),
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(ForbiddenError)
async def forbidden_handler(_request: Request, exc: ForbiddenError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=error_response(exc.message, exc.details),
    )


@app.exception_handler(ConflictError)
async def conflict_handler(_request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response(exc.message, exc.details),
    )


@app.exception_handler(ValidationError)
async def validation_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(exc.message, exc.details),
    )


@app.exception_handler(BadRequestError)
async def bad_request_handler(_request: Request, exc: BadRequestError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response(exc.message, exc.details),
    )


@app.exception_handler(EstimateAIException)
async def app_exception_handler(_request: Request, exc: EstimateAIException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(exc.message, exc.details),
    )


@app.exception_handler(RequestValidationError)
async def pydantic_validation_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            "Request validation failed",
            {"errors": exc.errors()},
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: {}", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response("Internal server error"),
    )


# --- API routers ---
# Each feature module exposes its own router (presentation layer)

app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(users_router, prefix=API_V1_PREFIX)
app.include_router(projects_router, prefix=API_V1_PREFIX)
app.include_router(pdf_router, prefix=API_V1_PREFIX)
app.include_router(measurements_router, prefix=API_V1_PREFIX)
app.include_router(markups_router, prefix=API_V1_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Liveness probe for Docker and load balancers."""
    return {"status": "healthy", "app": settings.app_name}
