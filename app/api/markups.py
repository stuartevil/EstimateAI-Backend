"""Markup endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schema.markup import MarkupCreate, MarkupResponse, MarkupUpdate
from app.service.markup_service import MarkupService
from app.utils.dependencies import get_current_active_user
from app.utils.response import APIResponse, success_response

router = APIRouter(prefix="/markups", tags=["Markups"])


def get_markup_service(db: AsyncSession = Depends(get_db)) -> MarkupService:
    return MarkupService(db)


@router.post(
    "/projects/{project_id}",
    response_model=APIResponse[MarkupResponse],
    status_code=201,
)
async def create_markup(
    project_id: UUID,
    payload: MarkupCreate,
    service: MarkupService = Depends(get_markup_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    markup = await service.create_markup(project_id, payload, owner_id=current_user.id)
    return success_response(
        data=MarkupResponse.model_validate(markup),
        message="Markup created",
    )


@router.get("/projects/{project_id}", response_model=APIResponse[list[MarkupResponse]])
async def list_markups(
    project_id: UUID,
    service: MarkupService = Depends(get_markup_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    markups = await service.list_markups(project_id, owner_id=current_user.id)
    return success_response(
        data=[MarkupResponse.model_validate(m) for m in markups],
        message="Markups retrieved",
    )


@router.get("/{markup_id}", response_model=APIResponse[MarkupResponse])
async def get_markup(
    markup_id: UUID,
    service: MarkupService = Depends(get_markup_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    markup = await service.get_markup(markup_id, owner_id=current_user.id)
    return success_response(
        data=MarkupResponse.model_validate(markup),
        message="Markup retrieved",
    )


@router.patch("/{markup_id}", response_model=APIResponse[MarkupResponse])
async def update_markup(
    markup_id: UUID,
    payload: MarkupUpdate,
    service: MarkupService = Depends(get_markup_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    markup = await service.update_markup(markup_id, payload, owner_id=current_user.id)
    return success_response(
        data=MarkupResponse.model_validate(markup),
        message="Markup updated",
    )


@router.delete("/{markup_id}", response_model=APIResponse[None])
async def delete_markup(
    markup_id: UUID,
    service: MarkupService = Depends(get_markup_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    await service.delete_markup(markup_id, owner_id=current_user.id)
    return success_response(data=None, message="Markup deleted")
