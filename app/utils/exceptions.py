"""Domain and application exceptions."""

from typing import Any


class EstimateAIException(Exception):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(EstimateAIException):
    pass


class ConflictError(EstimateAIException):
    pass


class UnauthorizedError(EstimateAIException):
    pass


class ForbiddenError(EstimateAIException):
    pass


class ValidationError(EstimateAIException):
    pass


class BadRequestError(EstimateAIException):
    pass
