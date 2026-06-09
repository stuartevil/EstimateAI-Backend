"""Project HTTP endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.projects.schema import ProjectCreate, ProjectResponse, ProjectUpdate
from app.modules.projects.service import ProjectService
from app.modules.users.model import User
from app.shared.dependencies import get_current_active_user
from app.shared.response import APIResponse, PaginatedData, success_response

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


@router.post("", response_model=APIResponse[ProjectResponse], status_code=201)
async def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Create a new estimation project."""
    project = await service.create_project(payload, owner_id=current_user.id)
    return success_response(
        data=ProjectResponse.model_validate(project),
        message="Project created",
    )


@router.get("", response_model=APIResponse[PaginatedData[ProjectResponse]])
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """List projects owned by the authenticated user."""
    skip = (page - 1) * page_size
    projects, total = await service.list_projects(
        owner_id=current_user.id,
        skip=skip,
        limit=page_size,
    )
    return success_response(
        data=PaginatedData(
            items=[ProjectResponse.model_validate(p) for p in projects],
            total=total,
            page=page,
            page_size=page_size,
        ),
        message="Projects retrieved",
    )


@router.get("/{project_id}", response_model=APIResponse[ProjectResponse])
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Get a project by ID."""
    project = await service.get_project(project_id, owner_id=current_user.id)
    return success_response(
        data=ProjectResponse.model_validate(project),
        message="Project retrieved",
    )


@router.patch("/{project_id}", response_model=APIResponse[ProjectResponse])
async def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Update a project."""
    project = await service.update_project(
        project_id,
        payload,
        owner_id=current_user.id,
    )
    return success_response(
        data=ProjectResponse.model_validate(project),
        message="Project updated",
    )


@router.delete("/{project_id}", response_model=APIResponse[None])
async def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Delete a project and all associated data."""
    await service.delete_project(project_id, owner_id=current_user.id)
    return success_response(data=None, message="Project deleted")
