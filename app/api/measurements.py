"""Measurement endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schema.measurement import MeasurementCreate, MeasurementResponse, MeasurementUpdate
from app.service.measurement_service import MeasurementService
from app.utils.dependencies import get_current_active_user
from app.utils.response import APIResponse, success_response

router = APIRouter(prefix="/measurements", tags=["Measurements"])


def get_measurement_service(db: AsyncSession = Depends(get_db)) -> MeasurementService:
    return MeasurementService(db)


@router.post(
    "/projects/{project_id}",
    response_model=APIResponse[MeasurementResponse],
    status_code=201,
)
async def create_measurement(
    project_id: UUID,
    payload: MeasurementCreate,
    service: MeasurementService = Depends(get_measurement_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    measurement = await service.create_measurement(
        project_id, payload, owner_id=current_user.id
    )
    return success_response(
        data=MeasurementResponse.model_validate(measurement),
        message="Measurement created",
    )


@router.get(
    "/projects/{project_id}",
    response_model=APIResponse[list[MeasurementResponse]],
)
async def list_measurements(
    project_id: UUID,
    service: MeasurementService = Depends(get_measurement_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    measurements = await service.list_measurements(project_id, owner_id=current_user.id)
    return success_response(
        data=[MeasurementResponse.model_validate(m) for m in measurements],
        message="Measurements retrieved",
    )


@router.get("/{measurement_id}", response_model=APIResponse[MeasurementResponse])
async def get_measurement(
    measurement_id: UUID,
    service: MeasurementService = Depends(get_measurement_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    measurement = await service.get_measurement(measurement_id, owner_id=current_user.id)
    return success_response(
        data=MeasurementResponse.model_validate(measurement),
        message="Measurement retrieved",
    )


@router.patch("/{measurement_id}", response_model=APIResponse[MeasurementResponse])
async def update_measurement(
    measurement_id: UUID,
    payload: MeasurementUpdate,
    service: MeasurementService = Depends(get_measurement_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    measurement = await service.update_measurement(
        measurement_id, payload, owner_id=current_user.id
    )
    return success_response(
        data=MeasurementResponse.model_validate(measurement),
        message="Measurement updated",
    )


@router.delete("/{measurement_id}", response_model=APIResponse[None])
async def delete_measurement(
    measurement_id: UUID,
    service: MeasurementService = Depends(get_measurement_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    await service.delete_measurement(measurement_id, owner_id=current_user.id)
    return success_response(data=None, message="Measurement deleted")
