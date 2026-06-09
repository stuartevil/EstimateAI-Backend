"""
Standard API response envelope.

All endpoints return a consistent shape so clients can handle success and
error uniformly without parsing framework-specific error bodies.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Uniform success/error response wrapper."""

    success: bool = True
    message: str = "OK"
    data: T | None = None


class PaginatedData(BaseModel, Generic[T]):
    """Pagination metadata wrapper for list endpoints."""

    items: list[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20


def success_response(
    data: Any = None,
    message: str = "OK",
) -> dict[str, Any]:
    """Build a standard success response dict."""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a standard error response dict."""
    return {
        "success": False,
        "message": message,
        "data": details,
    }
