from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.takeoff import Takeoff


class TakeoffRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, takeoff_id: UUID) -> Takeoff | None:
        result = await self.session.execute(select(Takeoff).where(Takeoff.id == takeoff_id))
        return result.scalar_one_or_none()

    async def create(self, takeoff: Takeoff) -> Takeoff:
        self.session.add(takeoff)
        await self.session.flush()
        await self.session.refresh(takeoff)
        return takeoff

    async def update(self, takeoff: Takeoff) -> Takeoff:
        await self.session.flush()
        await self.session.refresh(takeoff)
        return takeoff

    async def delete(self, takeoff: Takeoff) -> None:
        await self.session.delete(takeoff)
        await self.session.flush()

    async def list_by_project(self, project_id: UUID) -> list[Takeoff]:
        result = await self.session.execute(
            select(Takeoff)
            .where(Takeoff.project_id == project_id)
            .order_by(Takeoff.created_at.desc())
        )
        return list(result.scalars().all())
