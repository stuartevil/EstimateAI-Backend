from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DrawingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    project_id: UUID
    filename: str
    original_filename: str
    file_size: int
    page_count: int
    mime_type: str
    thumbnail_path: str | None = None
    created_at: datetime
    preview_path: str | None = None
    status: str = "uploaded"


class DrawingUploadResponse(DrawingResponse):
    message: str = Field(default="Drawing uploaded successfully")
