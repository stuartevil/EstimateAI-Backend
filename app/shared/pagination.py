"""Pagination helpers."""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedData(BaseModel, Generic[T]):
    items: list[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20


def paginate(items: list[T], total: int, page: int, page_size: int) -> PaginatedData[T]:
    return PaginatedData(items=items, total=total, page=page, page_size=page_size)
