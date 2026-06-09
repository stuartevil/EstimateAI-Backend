"""PDF request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PDFDocumentResponse(BaseModel):
    """Public PDF document representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    filename: str
    original_filename: str
    file_size: int
    page_count: int
    mime_type: str
    created_at: datetime


class PDFUploadResponse(PDFDocumentResponse):
    """Response after successful PDF upload."""

    message: str = Field(default="PDF uploaded successfully")
