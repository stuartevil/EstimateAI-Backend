from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.drawing_schema import DrawingResponse, DrawingUploadResponse
from app.services.drawing_service import DrawingService
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/drawings", tags=["Drawings"])


def get_drawing_service(db: AsyncSession = Depends(get_db)) -> DrawingService:
    return DrawingService(db)


@router.post("/projects/{project_id}/upload", response_model=APIResponse[DrawingUploadResponse], status_code=201)
async def upload_drawing(
    project_id: UUID,
    file: UploadFile = File(...),
    service: DrawingService = Depends(get_drawing_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    drawing = await service.upload_drawing(project_id, file, owner_id=current_user.id)
    return success_response(data=DrawingUploadResponse.model_validate(drawing), message="Drawing uploaded")


@router.get("/projects/{project_id}", response_model=APIResponse[list[DrawingResponse]])
async def list_drawings(
    project_id: UUID,
    service: DrawingService = Depends(get_drawing_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    drawings = await service.list_drawings(project_id, owner_id=current_user.id)
    return success_response(
        data=[DrawingResponse.model_validate(d) for d in drawings],
        message="Drawings retrieved",
    )


@router.get("/{drawing_id}", response_model=APIResponse[DrawingResponse])
async def get_drawing(
    drawing_id: UUID,
    service: DrawingService = Depends(get_drawing_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    drawing = await service.get_drawing(drawing_id, owner_id=current_user.id)
    return success_response(data=DrawingResponse.model_validate(drawing), message="Drawing retrieved")


@router.delete("/{drawing_id}", response_model=APIResponse[None])
async def delete_drawing(
    drawing_id: UUID,
    service: DrawingService = Depends(get_drawing_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    await service.delete_drawing(drawing_id, owner_id=current_user.id)
    return success_response(data=None, message="Drawing deleted")
