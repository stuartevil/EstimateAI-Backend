from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import TAKEOFF_STATUSES
from app.models.takeoff import Takeoff
from app.repositories.takeoff_repository import TakeoffRepository
from app.schemas.takeoff_schema import TakeoffCreate, TakeoffUpdate
from app.services.project_service import ProjectService
from app.shared.exceptions import NotFoundError, ValidationError


class TakeoffService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = TakeoffRepository(session)
        self.project_service = ProjectService(session)

    def _validate_status(self, status: str) -> None:
        if status not in TAKEOFF_STATUSES:
            raise ValidationError(f"Invalid takeoff status. Allowed: {', '.join(TAKEOFF_STATUSES)}")

    async def create_takeoff(self, project_id: UUID, data: TakeoffCreate, owner_id: UUID) -> Takeoff:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        self._validate_status(data.status)
        takeoff = Takeoff(
            project_id=project_id,
            name=data.name,
            status=data.status,
            created_by=owner_id,
        )
        return await self.repo.create(takeoff)

    async def get_takeoff(self, takeoff_id: UUID, owner_id: UUID) -> Takeoff:
        takeoff = await self.repo.get_by_id(takeoff_id)
        if takeoff is None:
            raise NotFoundError("Takeoff not found")
        await self.project_service.get_project(takeoff.project_id, owner_id=owner_id)
        return takeoff

    async def list_takeoffs(self, project_id: UUID, owner_id: UUID) -> list[Takeoff]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        return await self.repo.list_by_project(project_id)

    async def update_takeoff(
        self, takeoff_id: UUID, data: TakeoffUpdate, owner_id: UUID
    ) -> Takeoff:
        takeoff = await self.get_takeoff(takeoff_id, owner_id=owner_id)
        if data.name is not None:
            takeoff.name = data.name
        if data.status is not None:
            self._validate_status(data.status)
            takeoff.status = data.status
        return await self.repo.update(takeoff)

    async def delete_takeoff(self, takeoff_id: UUID, owner_id: UUID) -> None:
        takeoff = await self.get_takeoff(takeoff_id, owner_id=owner_id)
        await self.repo.delete(takeoff)
