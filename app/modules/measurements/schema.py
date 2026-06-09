"""Measurement request/response schemas."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.shared.constants import MEASUREMENT_TYPES


class MeasurementBase(BaseModel):
    """Shared measurement fields."""

    page_number: int = Field(default=0, ge=0)
    measurement_type: str = Field(..., description=f"One of: {MEASUREMENT_TYPES}")
    label: str = Field(..., min_length=1, max_length=255)
    value: float = Field(default=0.0, ge=0)
    unit: str = Field(default="ft", max_length=50)
    geometry: dict[str, Any] = Field(default_factory=dict)
    pdf_document_id: UUID | None = None


class MeasurementCreate(MeasurementBase):
    """Schema for creating a measurement."""


class MeasurementUpdate(BaseModel):
    """Schema for partial measurement updates."""

    page_number: int | None = Field(default=None, ge=0)
    measurement_type: str | None = None
    label: str | None = Field(default=None, min_length=1, max_length=255)
    value: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, max_length=50)
    geometry: dict[str, Any] | None = None
    pdf_document_id: UUID | None = None


class MeasurementResponse(MeasurementBase):
    """Public measurement representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    created_by: UUID | None
    created_at: datetime
