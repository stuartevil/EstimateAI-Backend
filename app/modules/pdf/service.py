"""
PDF upload and management business logic.

Orchestrates file storage, validation, and metadata persistence.
"""

import uuid
from pathlib import Path

from fastapi import UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.modules.pdf.model import PDFDocument
from app.modules.pdf.pdf_processor import PDFProcessor
from app.modules.pdf.repository import PDFRepository
from app.modules.projects.service import ProjectService
from app.shared.constants import ALLOWED_PDF_MIME_TYPES
from app.shared.exceptions import BadRequestError, NotFoundError

settings = get_settings()


class PDFService:
    """PDF document domain service."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = PDFRepository(session)
        self.project_service = ProjectService(session)
        self.processor = PDFProcessor()
        self.upload_dir = settings.upload_dir

    def _ensure_upload_dir(self, project_id: uuid.UUID) -> Path:
        """Create project-specific upload directory if missing."""
        project_dir = self.upload_dir / str(project_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    async def upload_pdf(
        self,
        project_id: uuid.UUID,
        file: UploadFile,
        owner_id: uuid.UUID,
    ) -> PDFDocument:
        """Upload, validate, and persist a PDF document."""
        # Verify project ownership before accepting upload
        await self.project_service.get_project(project_id, owner_id=owner_id)

        if file.content_type not in ALLOWED_PDF_MIME_TYPES:
            raise BadRequestError(
                f"Invalid file type. Allowed: {', '.join(ALLOWED_PDF_MIME_TYPES)}"
            )

        content = await file.read()
        if len(content) == 0:
            raise BadRequestError("Empty file uploaded")
        if len(content) > settings.max_upload_size_bytes:
            raise BadRequestError(
                f"File exceeds maximum size of {settings.max_upload_size_mb} MB"
            )

        project_dir = self._ensure_upload_dir(project_id)
        stored_filename = f"{uuid.uuid4()}.pdf"
        file_path = project_dir / stored_filename

        file_path.write_bytes(content)
        logger.info("PDF saved to {}", file_path)

        try:
            page_count = self.processor.extract_page_count(file_path)
        except Exception:
            file_path.unlink(missing_ok=True)
            raise

        document = PDFDocument(
            project_id=project_id,
            filename=stored_filename,
            original_filename=file.filename or stored_filename,
            file_path=str(file_path),
            file_size=len(content),
            page_count=page_count,
            mime_type=file.content_type or "application/pdf",
        )
        return await self.repo.create(document)

    async def get_document(
        self,
        document_id: uuid.UUID,
        owner_id: uuid.UUID,
    ) -> PDFDocument:
        document = await self.repo.get_by_id(document_id)
        if document is None:
            raise NotFoundError("PDF document not found")
        await self.project_service.get_project(document.project_id, owner_id=owner_id)
        return document

    async def list_documents(
        self,
        project_id: uuid.UUID,
        owner_id: uuid.UUID,
    ) -> list[PDFDocument]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        return await self.repo.list_by_project(project_id)

    async def delete_document(
        self,
        document_id: uuid.UUID,
        owner_id: uuid.UUID,
    ) -> None:
        document = await self.get_document(document_id, owner_id=owner_id)
        Path(document.file_path).unlink(missing_ok=True)
        await self.repo.delete(document)
