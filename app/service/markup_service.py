"""Markup business logic."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.markup import Markup
from app.schema.markup import MarkupCreate, MarkupUpdate
from app.service.markup_repository import MarkupRepository
from app.service.project_service import ProjectService
from app.utils.constants import MARKUP_TYPES
from app.utils.exceptions import NotFoundError, ValidationError


class MarkupService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = MarkupRepository(session)
        self.project_service = ProjectService(session)

    def _validate_type(self, markup_type: str) -> None:
        if markup_type not in MARKUP_TYPES:
            raise ValidationError(
                f"Invalid markup type. Allowed: {', '.join(MARKUP_TYPES)}"
            )

    async def create_markup(
        self, project_id: UUID, data: MarkupCreate, owner_id: UUID
    ) -> Markup:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        self._validate_type(data.markup_type)

        markup = Markup(
            project_id=project_id,
            pdf_document_id=data.pdf_document_id,
            page_number=data.page_number,
            markup_type=data.markup_type,
            content=data.content,
            properties=data.properties,
            created_by=owner_id,
        )
        return await self.repo.create(markup)

    async def get_markup(self, markup_id: UUID, owner_id: UUID) -> Markup:
        markup = await self.repo.get_by_id(markup_id)
        if markup is None:
            raise NotFoundError("Markup not found")
        await self.project_service.get_project(markup.project_id, owner_id=owner_id)
        return markup

    async def list_markups(self, project_id: UUID, owner_id: UUID) -> list[Markup]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        return await self.repo.list_by_project(project_id)

    async def update_markup(
        self, markup_id: UUID, data: MarkupUpdate, owner_id: UUID
    ) -> Markup:
        markup = await self.get_markup(markup_id, owner_id=owner_id)

        if data.markup_type is not None:
            self._validate_type(data.markup_type)
            markup.markup_type = data.markup_type
        if data.page_number is not None:
            markup.page_number = data.page_number
        if data.content is not None:
            markup.content = data.content
        if data.properties is not None:
            markup.properties = data.properties
        if data.pdf_document_id is not None:
            markup.pdf_document_id = data.pdf_document_id

        return await self.repo.update(markup)

    async def delete_markup(self, markup_id: UUID, owner_id: UUID) -> None:
        markup = await self.get_markup(markup_id, owner_id=owner_id)
        await self.repo.delete(markup)
