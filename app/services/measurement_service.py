from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import MEASUREMENT_TYPES
from app.models.measurement import Measurement
from app.repositories.measurement_repository import MeasurementRepository
from app.schemas.measurement_schema import MeasurementCreate, MeasurementUpdate
from app.services.project_service import ProjectService
from app.shared.exceptions import NotFoundError, ValidationError


class MeasurementService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = MeasurementRepository(session)
        self.project_service = ProjectService(session)

    def _validate_type(self, measurement_type: str) -> None:
        if measurement_type not in MEASUREMENT_TYPES:
            raise ValidationError(
                f"Invalid measurement type. Allowed: {', '.join(MEASUREMENT_TYPES)}"
            )

    async def create_measurement(
        self, project_id: UUID, data: MeasurementCreate, owner_id: UUID
    ) -> Measurement:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        self._validate_type(data.measurement_type)
        measurement = Measurement(
            project_id=project_id,
            takeoff_id=data.takeoff_id,
            drawing_id=data.drawing_id,
            page_number=data.page_number,
            measurement_type=data.measurement_type,
            label=data.label,
            value=data.value,
            unit=data.unit,
            geometry=data.geometry,
            created_by=owner_id,
        )
        return await self.repo.create(measurement)

    async def get_measurement(self, measurement_id: UUID, owner_id: UUID) -> Measurement:
        measurement = await self.repo.get_by_id(measurement_id)
        if measurement is None:
            raise NotFoundError("Measurement not found")
        await self.project_service.get_project(measurement.project_id, owner_id=owner_id)
        return measurement

    async def list_measurements(self, project_id: UUID, owner_id: UUID) -> list[Measurement]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        return await self.repo.list_by_project(project_id)

    async def update_measurement(
        self, measurement_id: UUID, data: MeasurementUpdate, owner_id: UUID
    ) -> Measurement:
        measurement = await self.get_measurement(measurement_id, owner_id=owner_id)
        if data.measurement_type is not None:
            self._validate_type(data.measurement_type)
            measurement.measurement_type = data.measurement_type
        if data.page_number is not None:
            measurement.page_number = data.page_number
        if data.label is not None:
            measurement.label = data.label
        if data.value is not None:
            measurement.value = data.value
        if data.unit is not None:
            measurement.unit = data.unit
        if data.geometry is not None:
            measurement.geometry = data.geometry
        if data.drawing_id is not None:
            measurement.drawing_id = data.drawing_id
        if data.takeoff_id is not None:
            measurement.takeoff_id = data.takeoff_id
        return await self.repo.update(measurement)

    async def delete_measurement(self, measurement_id: UUID, owner_id: UUID) -> None:
        measurement = await self.get_measurement(measurement_id, owner_id=owner_id)
        await self.repo.delete(measurement)
