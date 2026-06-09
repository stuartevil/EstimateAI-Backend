"""Measurement data access layer."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.measurements.model import Measurement


class MeasurementRepository:
    """CRUD operations for Measurement entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, measurement_id: UUID) -> Measurement | None:
        result = await self.session.execute(
            select(Measurement).where(Measurement.id == measurement_id)
        )
        return result.scalar_one_or_none()

    async def create(self, measurement: Measurement) -> Measurement:
        self.session.add(measurement)
        await self.session.flush()
        await self.session.refresh(measurement)
        return measurement

    async def update(self, measurement: Measurement) -> Measurement:
        await self.session.flush()
        await self.session.refresh(measurement)
        return measurement

    async def delete(self, measurement: Measurement) -> None:
        await self.session.delete(measurement)
        await self.session.flush()

    async def list_by_project(self, project_id: UUID) -> list[Measurement]:
        result = await self.session.execute(
            select(Measurement)
            .where(Measurement.project_id == project_id)
            .order_by(Measurement.created_at.desc())
        )
        return list(result.scalars().all())
