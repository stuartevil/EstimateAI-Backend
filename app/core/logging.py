"""
Loguru logging configuration.

Centralized logging with console + rotating file sinks.
Call setup_logging() once at application startup.
"""

import sys

from loguru import logger

from app.core.config import get_settings


def setup_logging() -> None:
    """Configure Loguru with rotation and structured output."""
    settings = get_settings()

    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    settings.log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        settings.log_file,
        level=settings.log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} | {message}"
        ),
    )

    logger.info("Logging initialized for {}", settings.app_name)
