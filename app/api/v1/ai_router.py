from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import AI_JOB_TYPES
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.services.ai_service import AIService
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/ai", tags=["AI"])


class AIJobCreateRequest(BaseModel):
    job_type: str = Field(..., description=f"One of: {AI_JOB_TYPES}")
    drawing_id: UUID | None = None
    input_payload: dict = Field(default_factory=dict)


class AIJobResponse(BaseModel):
    id: UUID
    project_id: UUID
    drawing_id: UUID | None
    job_type: str
    status: str

    model_config = {"from_attributes": True}


def get_ai_service(db: AsyncSession = Depends(get_db)) -> AIService:
    return AIService(db)


@router.post("/projects/{project_id}/jobs", response_model=APIResponse[AIJobResponse], status_code=201)
async def create_ai_job(
    project_id: UUID,
    payload: AIJobCreateRequest,
    service: AIService = Depends(get_ai_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    job = await service.create_job(
        project_id=project_id,
        job_type=payload.job_type,
        owner_id=current_user.id,
        drawing_id=payload.drawing_id,
        input_payload=payload.input_payload,
    )
    return success_response(data=AIJobResponse.model_validate(job), message="AI job created")


@router.get("/projects/{project_id}/jobs", response_model=APIResponse[list[AIJobResponse]])
async def list_ai_jobs(
    project_id: UUID,
    service: AIService = Depends(get_ai_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    jobs = await service.list_jobs(project_id, owner_id=current_user.id)
    return success_response(
        data=[AIJobResponse.model_validate(j) for j in jobs],
        message="AI jobs retrieved",
    )


@router.get("/jobs/{job_id}", response_model=APIResponse[AIJobResponse])
async def get_ai_job(
    job_id: UUID,
    service: AIService = Depends(get_ai_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    job = await service.get_job(job_id, owner_id=current_user.id)
    return success_response(data=AIJobResponse.model_validate(job), message="AI job retrieved")
