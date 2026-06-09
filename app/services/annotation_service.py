from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import MARKUP_TYPES
from app.models.annotation import Annotation
from app.repositories.annotation_repository import AnnotationRepository
from app.schemas.annotation_schema import AnnotationCreate, AnnotationUpdate
from app.services.project_service import ProjectService
from app.shared.exceptions import NotFoundError, ValidationError


class AnnotationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = AnnotationRepository(session)
        self.project_service = ProjectService(session)

    def _validate_type(self, annotation_type: str) -> None:
        if annotation_type not in MARKUP_TYPES:
            raise ValidationError(f"Invalid annotation type. Allowed: {', '.join(MARKUP_TYPES)}")

    async def create_annotation(
        self, project_id: UUID, data: AnnotationCreate, owner_id: UUID
    ) -> Annotation:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        self._validate_type(data.annotation_type)
        annotation = Annotation(
            project_id=project_id,
            drawing_id=data.drawing_id,
            page_number=data.page_number,
            annotation_type=data.annotation_type,
            content=data.content,
            properties=data.properties,
            created_by=owner_id,
        )
        return await self.repo.create(annotation)

    async def get_annotation(self, annotation_id: UUID, owner_id: UUID) -> Annotation:
        annotation = await self.repo.get_by_id(annotation_id)
        if annotation is None:
            raise NotFoundError("Annotation not found")
        await self.project_service.get_project(annotation.project_id, owner_id=owner_id)
        return annotation

    async def list_annotations(self, project_id: UUID, owner_id: UUID) -> list[Annotation]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        return await self.repo.list_by_project(project_id)

    async def update_annotation(
        self, annotation_id: UUID, data: AnnotationUpdate, owner_id: UUID
    ) -> Annotation:
        annotation = await self.get_annotation(annotation_id, owner_id=owner_id)
        if data.annotation_type is not None:
            self._validate_type(data.annotation_type)
            annotation.annotation_type = data.annotation_type
        if data.page_number is not None:
            annotation.page_number = data.page_number
        if data.content is not None:
            annotation.content = data.content
        if data.properties is not None:
            annotation.properties = data.properties
        if data.drawing_id is not None:
            annotation.drawing_id = data.drawing_id
        return await self.repo.update(annotation)

    async def delete_annotation(self, annotation_id: UUID, owner_id: UUID) -> None:
        annotation = await self.get_annotation(annotation_id, owner_id=owner_id)
        await self.repo.delete(annotation)
