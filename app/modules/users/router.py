"""
User HTTP endpoints.

Routers are thin — they delegate to services and wrap responses.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.users.schema import UserResponse, UserUpdate
from app.modules.users.service import UserService
from app.shared.dependencies import get_current_active_user
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(
    current_user=Depends(get_current_active_user),
) -> dict:
    """Return the authenticated user's profile."""
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
    """Get a user by ID."""
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
    """Update the authenticated user's profile."""
    user = await service.update_user(current_user.id, payload)
    return success_response(
        data=UserResponse.model_validate(user),
        message="User updated",
    )
