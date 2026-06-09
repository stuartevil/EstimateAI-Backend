from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.annotation_schema import AnnotationCreate, AnnotationResponse, AnnotationUpdate
from app.services.annotation_service import AnnotationService
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/annotations", tags=["Annotations"])


def get_annotation_service(db: AsyncSession = Depends(get_db)) -> AnnotationService:
    return AnnotationService(db)


@router.post("/projects/{project_id}", response_model=APIResponse[AnnotationResponse], status_code=201)
async def create_annotation(
    project_id: UUID,
    payload: AnnotationCreate,
    service: AnnotationService = Depends(get_annotation_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    annotation = await service.create_annotation(project_id, payload, owner_id=current_user.id)
    return success_response(data=AnnotationResponse.model_validate(annotation), message="Annotation created")


@router.get("/projects/{project_id}", response_model=APIResponse[list[AnnotationResponse]])
async def list_annotations(
    project_id: UUID,
    service: AnnotationService = Depends(get_annotation_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    annotations = await service.list_annotations(project_id, owner_id=current_user.id)
    return success_response(
        data=[AnnotationResponse.model_validate(a) for a in annotations],
        message="Annotations retrieved",
    )


@router.get("/{annotation_id}", response_model=APIResponse[AnnotationResponse])
async def get_annotation(
    annotation_id: UUID,
    service: AnnotationService = Depends(get_annotation_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    annotation = await service.get_annotation(annotation_id, owner_id=current_user.id)
    return success_response(data=AnnotationResponse.model_validate(annotation), message="Annotation retrieved")


@router.patch("/{annotation_id}", response_model=APIResponse[AnnotationResponse])
async def update_annotation(
    annotation_id: UUID,
    payload: AnnotationUpdate,
    service: AnnotationService = Depends(get_annotation_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    annotation = await service.update_annotation(annotation_id, payload, owner_id=current_user.id)
    return success_response(data=AnnotationResponse.model_validate(annotation), message="Annotation updated")


@router.delete("/{annotation_id}", response_model=APIResponse[None])
async def delete_annotation(
    annotation_id: UUID,
    service: AnnotationService = Depends(get_annotation_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    await service.delete_annotation(annotation_id, owner_id=current_user.id)
    return success_response(data=None, message="Annotation deleted")
