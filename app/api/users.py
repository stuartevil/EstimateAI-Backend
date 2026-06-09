"""User endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schema.user import UserResponse, UserUpdate
from app.service.user_service import UserService
from app.utils.dependencies import get_current_active_user
from app.utils.response import APIResponse, success_response

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(current_user=Depends(get_current_active_user)) -> dict:
    return success_response(
        data=UserResponse.model_validate(current_user),
        message="User profile retrieved",
    )


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    _current_user=Depends(get_current_active_user),
) -> dict:
    user = await service.get_user(user_id)
    return success_response(
        data=UserResponse.model_validate(user),
        message="User retrieved",
    )


@router.patch("/me", response_model=APIResponse[UserResponse])
async def update_me(
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_active_user),
) -> dict:
    user = await service.update_user(current_user.id, payload)
    return success_response(
        data=UserResponse.model_validate(user),
        message="User updated",
    )
