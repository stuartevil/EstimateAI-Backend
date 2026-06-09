import uuid
from pathlib import Path

from fastapi import UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.constants import ALLOWED_PDF_MIME_TYPES
from app.models.drawing import Drawing
from app.modules.pdf_engine.pdf_processor import PDFProcessor
from app.modules.pdf_engine.thumbnail_generator import ThumbnailGenerator
from app.repositories.drawing_repository import DrawingRepository
from app.services.project_service import ProjectService
from app.shared.exceptions import BadRequestError, NotFoundError

settings = get_settings()


class DrawingService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = DrawingRepository(session)
        self.project_service = ProjectService(session)
        self.processor = PDFProcessor()
        self.thumbnail_gen = ThumbnailGenerator()

    def _storage_path(self, project_id: uuid.UUID) -> Path:
        path = settings.storage_original / str(project_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    async def upload_drawing(
        self, project_id: uuid.UUID, file: UploadFile, owner_id: uuid.UUID
    ) -> Drawing:
        await self.project_service.get_project(project_id, owner_id=owner_id)

        if file.content_type not in ALLOWED_PDF_MIME_TYPES:
            raise BadRequestError(f"Invalid file type. Allowed: {', '.join(ALLOWED_PDF_MIME_TYPES)}")

        content = await file.read()
        if not content:
            raise BadRequestError("Empty file uploaded")
        if len(content) > settings.max_upload_size_bytes:
            raise BadRequestError(f"File exceeds maximum size of {settings.max_upload_size_mb} MB")

        storage_dir = self._storage_path(project_id)
        stored_filename = f"{uuid.uuid4()}.pdf"
        file_path = storage_dir / stored_filename
        file_path.write_bytes(content)
        logger.info("Drawing saved to {}", file_path)

        thumbnail_path = None

        try:
            page_count = self.processor.extract_page_count(file_path)
            thumbnail_path = self.thumbnail_gen.generate(file_path, project_id)

        except Exception as e:
            logger.exception("Failed processing drawing: {}", e)

            # Remove uploaded PDF if processing fails
            file_path.unlink(missing_ok=True)

            # Remove thumbnail if it was created
            if thumbnail_path:
                Path(thumbnail_path).unlink(missing_ok=True)

            raise

        drawing = Drawing(
            project_id=project_id,
            filename=stored_filename,
            original_filename=file.filename or stored_filename,
            file_path=str(file_path),
            thumbnail_path=str(thumbnail_path) if thumbnail_path else None,
            file_size=len(content),
            page_count=page_count,
            mime_type=file.content_type or "application/pdf",
        )
        return await self.repo.create(drawing)

    async def get_drawing(self, drawing_id: uuid.UUID, owner_id: uuid.UUID) -> Drawing:
        drawing = await self.repo.get_by_id(drawing_id)
        if drawing is None:
            raise NotFoundError("Drawing not found")
        await self.project_service.get_project(drawing.project_id, owner_id=owner_id)
        return drawing

    async def list_drawings(self, project_id: uuid.UUID, owner_id: uuid.UUID) -> list[Drawing]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        return await self.repo.list_by_project(project_id)

    async def delete_drawing(self, drawing_id: uuid.UUID, owner_id: uuid.UUID) -> None:
        drawing = await self.get_drawing(drawing_id, owner_id=owner_id)
        Path(drawing.file_path).unlink(missing_ok=True)
        if drawing.thumbnail_path:
            Path(drawing.thumbnail_path).unlink(missing_ok=True)
        await self.repo.delete(drawing)
