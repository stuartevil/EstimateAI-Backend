from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import TAKEOFF_STATUSES


class TakeoffBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    status: str = Field(default="draft", description=f"One of: {TAKEOFF_STATUSES}")


class TakeoffCreate(TakeoffBase):
    pass


class TakeoffUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status: str | None = None


class TakeoffResponse(TakeoffBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    project_id: UUID
    created_by: UUID | None
    created_at: datetime
