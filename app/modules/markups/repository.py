"""Markup data access layer."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.markups.model import Markup


class MarkupRepository:
    """CRUD operations for Markup entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, markup_id: UUID) -> Markup | None:
        result = await self.session.execute(select(Markup).where(Markup.id == markup_id))
        return result.scalar_one_or_none()

    async def create(self, markup: Markup) -> Markup:
        self.session.add(markup)
        await self.session.flush()
        await self.session.refresh(markup)
        return markup

    async def update(self, markup: Markup) -> Markup:
        await self.session.flush()
        await self.session.refresh(markup)
        return markup

    async def delete(self, markup: Markup) -> None:
        await self.session.delete(markup)
        await self.session.flush()

    async def list_by_project(self, project_id: UUID) -> list[Markup]:
        result = await self.session.execute(
            select(Markup)
            .where(Markup.project_id == project_id)
            .order_by(Markup.created_at.desc())
        )
        return list(result.scalars().all())
