from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import MARKUP_TYPES


class AnnotationBase(BaseModel):
    page_number: int = Field(default=0, ge=0)
    annotation_type: str = Field(..., description=f"One of: {MARKUP_TYPES}")
    content: str | None = Field(default=None, max_length=2000)
    properties: dict[str, Any] = Field(default_factory=dict)
    drawing_id: UUID | None = None


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationUpdate(BaseModel):
    page_number: int | None = Field(default=None, ge=0)
    annotation_type: str | None = None
    content: str | None = Field(default=None, max_length=2000)
    properties: dict[str, Any] | None = None
    drawing_id: UUID | None = None


class AnnotationResponse(AnnotationBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    project_id: UUID
    created_by: UUID | None
    created_at: datetime
