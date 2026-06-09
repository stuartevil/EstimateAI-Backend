from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.takeoff_schema import TakeoffCreate, TakeoffResponse, TakeoffUpdate
from app.services.takeoff_service import TakeoffService
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/takeoffs", tags=["Takeoffs"])


def get_takeoff_service(db: AsyncSession = Depends(get_db)) -> TakeoffService:
    return TakeoffService(db)


@router.post("/projects/{project_id}", response_model=APIResponse[TakeoffResponse], status_code=201)
async def create_takeoff(
    project_id: UUID,
    payload: TakeoffCreate,
    service: TakeoffService = Depends(get_takeoff_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    takeoff = await service.create_takeoff(project_id, payload, owner_id=current_user.id)
    return success_response(data=TakeoffResponse.model_validate(takeoff), message="Takeoff created")


@router.get("/projects/{project_id}", response_model=APIResponse[list[TakeoffResponse]])
async def list_takeoffs(
    project_id: UUID,
    service: TakeoffService = Depends(get_takeoff_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    takeoffs = await service.list_takeoffs(project_id, owner_id=current_user.id)
    return success_response(
        data=[TakeoffResponse.model_validate(t) for t in takeoffs],
        message="Takeoffs retrieved",
    )


@router.get("/{takeoff_id}", response_model=APIResponse[TakeoffResponse])
async def get_takeoff(
    takeoff_id: UUID,
    service: TakeoffService = Depends(get_takeoff_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    takeoff = await service.get_takeoff(takeoff_id, owner_id=current_user.id)
    return success_response(data=TakeoffResponse.model_validate(takeoff), message="Takeoff retrieved")


@router.patch("/{takeoff_id}", response_model=APIResponse[TakeoffResponse])
async def update_takeoff(
    takeoff_id: UUID,
    payload: TakeoffUpdate,
    service: TakeoffService = Depends(get_takeoff_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    takeoff = await service.update_takeoff(takeoff_id, payload, owner_id=current_user.id)
    return success_response(data=TakeoffResponse.model_validate(takeoff), message="Takeoff updated")


@router.delete("/{takeoff_id}", response_model=APIResponse[None])
async def delete_takeoff(
    takeoff_id: UUID,
    service: TakeoffService = Depends(get_takeoff_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    await service.delete_takeoff(takeoff_id, owner_id=current_user.id)
    return success_response(data=None, message="Takeoff deleted")
