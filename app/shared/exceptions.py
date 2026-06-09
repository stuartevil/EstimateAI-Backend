"""
Domain and application exceptions.

Custom exceptions allow services to express business failures without
coupling to HTTP. Exception handlers in main.py map these to responses.
"""

from typing import Any


class EstimateAIException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(EstimateAIException):
    """Resource was not found."""


class ConflictError(EstimateAIException):
    """Resource already exists or state conflict."""


class UnauthorizedError(EstimateAIException):
    """Authentication failed."""


class ForbiddenError(EstimateAIException):
    """Authenticated but not permitted."""


class ValidationError(EstimateAIException):
    """Business validation failed."""


class BadRequestError(EstimateAIException):
    """Malformed or invalid request."""
