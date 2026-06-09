from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.annotation import Annotation


class AnnotationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, annotation_id: UUID) -> Annotation | None:
        result = await self.session.execute(
            select(Annotation).where(Annotation.id == annotation_id)
        )
        return result.scalar_one_or_none()

    async def create(self, annotation: Annotation) -> Annotation:
        self.session.add(annotation)
        await self.session.flush()
        await self.session.refresh(annotation)
        return annotation

    async def update(self, annotation: Annotation) -> Annotation:
        await self.session.flush()
        await self.session.refresh(annotation)
        return annotation

    async def delete(self, annotation: Annotation) -> None:
        await self.session.delete(annotation)
        await self.session.flush()

    async def list_by_project(self, project_id: UUID) -> list[Annotation]:
        result = await self.session.execute(
            select(Annotation)
            .where(Annotation.project_id == project_id)
            .order_by(Annotation.created_at.desc())
        )
        return list(result.scalars().all())
