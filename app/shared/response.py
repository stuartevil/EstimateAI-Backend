"""Standard API response envelope."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: T | None = None


def success_response(data: Any = None, message: str = "OK") -> dict[str, Any]:
    return {"success": True, "message": message, "data": data}


def error_response(message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"success": False, "message": message, "data": details}
