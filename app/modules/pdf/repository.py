"""PDF document data access layer."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.pdf.model import PDFDocument


class PDFRepository:
    """CRUD operations for PDFDocument entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, document_id: UUID) -> PDFDocument | None:
        result = await self.session.execute(
            select(PDFDocument).where(PDFDocument.id == document_id)
        )
        return result.scalar_one_or_none()

    async def create(self, document: PDFDocument) -> PDFDocument:
        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def delete(self, document: PDFDocument) -> None:
        await self.session.delete(document)
        await self.session.flush()

    async def list_by_project(self, project_id: UUID) -> list[PDFDocument]:
        result = await self.session.execute(
            select(PDFDocument)
            .where(PDFDocument.project_id == project_id)
            .order_by(PDFDocument.created_at.desc())
        )
        return list(result.scalars().all())
