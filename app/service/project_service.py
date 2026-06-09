"""Project business logic."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schema.project import ProjectCreate, ProjectUpdate
from app.service.project_repository import ProjectRepository
from app.utils.exceptions import ForbiddenError, NotFoundError


class ProjectService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = ProjectRepository(session)

    async def get_project(self, project_id: UUID, owner_id: UUID | None = None) -> Project:
        project = await self.repo.get_by_id(project_id)
        if project is None:
            raise NotFoundError("Project not found")
        if owner_id is not None and project.owner_id != owner_id:
            raise ForbiddenError("Not authorized to access this project")
        return project

    async def create_project(self, data: ProjectCreate, owner_id: UUID) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            owner_id=owner_id,
        )
        return await self.repo.create(project)

    async def update_project(
        self, project_id: UUID, data: ProjectUpdate, owner_id: UUID
    ) -> Project:
        project = await self.get_project(project_id, owner_id=owner_id)

        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description

        return await self.repo.update(project)

    async def delete_project(self, project_id: UUID, owner_id: UUID) -> None:
        project = await self.get_project(project_id, owner_id=owner_id)
        await self.repo.delete(project)

    async def list_projects(
        self, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> tuple[list[Project], int]:
        projects = await self.repo.list_by_owner(owner_id, skip=skip, limit=limit)
        total = await self.repo.count_by_owner(owner_id)
        return projects, total
