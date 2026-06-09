from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import MEASUREMENT_TYPES


class MeasurementBase(BaseModel):
    page_number: int = Field(default=0, ge=0)
    measurement_type: str = Field(..., description=f"One of: {MEASUREMENT_TYPES}")
    label: str = Field(..., min_length=1, max_length=255)
    value: float = Field(default=0.0, ge=0)
    unit: str = Field(default="ft", max_length=50)
    geometry: dict[str, Any] = Field(default_factory=dict)
    drawing_id: UUID | None = None
    takeoff_id: UUID | None = None


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementUpdate(BaseModel):
    page_number: int | None = Field(default=None, ge=0)
    measurement_type: str | None = None
    label: str | None = Field(default=None, min_length=1, max_length=255)
    value: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, max_length=50)
    geometry: dict[str, Any] | None = None
    drawing_id: UUID | None = None
    takeoff_id: UUID | None = None


class MeasurementResponse(MeasurementBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    project_id: UUID
    created_by: UUID | None
    created_at: datetime
