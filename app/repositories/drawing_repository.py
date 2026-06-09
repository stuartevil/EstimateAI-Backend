from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.drawing import Drawing


class DrawingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, drawing_id: UUID) -> Drawing | None:
        result = await self.session.execute(select(Drawing).where(Drawing.id == drawing_id))
        return result.scalar_one_or_none()

    async def create(self, drawing: Drawing) -> Drawing:
        self.session.add(drawing)
        await self.session.flush()
        await self.session.refresh(drawing)
        return drawing

    async def update(self, drawing: Drawing) -> Drawing:
        await self.session.flush()
        await self.session.refresh(drawing)
        return drawing

    async def delete(self, drawing: Drawing) -> None:
        await self.session.delete(drawing)
        await self.session.flush()

    async def list_by_project(self, project_id: UUID) -> list[Drawing]:
        result = await self.session.execute(
            select(Drawing)
            .where(Drawing.project_id == project_id)
            .order_by(Drawing.created_at.desc())
        )
        return list(result.scalars().all())
