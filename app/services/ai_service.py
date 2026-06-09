"""AI job orchestration service."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import AI_JOB_STATUSES, AI_JOB_TYPES
from app.models.ai_job import AIJob
from app.modules.ai.ai_markup_generator import AIMarkupGenerator
from app.modules.ai.ai_takeoff_generator import AITakeoffGenerator
from app.modules.jobs.task_queue import TaskQueue
from app.services.project_service import ProjectService
from app.shared.exceptions import NotFoundError, ValidationError


class AIService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.project_service = ProjectService(session)
        self.task_queue = TaskQueue()
        self.markup_generator = AIMarkupGenerator()
        self.takeoff_generator = AITakeoffGenerator()

    def _validate_job_type(self, job_type: str) -> None:
        if job_type not in AI_JOB_TYPES:
            raise ValidationError(f"Invalid job type. Allowed: {', '.join(AI_JOB_TYPES)}")

    async def create_job(
        self,
        project_id: UUID,
        job_type: str,
        owner_id: UUID,
        drawing_id: UUID | None = None,
        input_payload: dict | None = None,
    ) -> AIJob:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        self._validate_job_type(job_type)

        job = AIJob(
            project_id=project_id,
            drawing_id=drawing_id,
            job_type=job_type,
            status="pending",
            input_payload=input_payload or {},
            created_by=owner_id,
        )
        self.session.add(job)
        await self.session.flush()
        await self.session.refresh(job)

        await self.task_queue.enqueue(job.id, job_type)
        return job

    async def get_job(self, job_id: UUID, owner_id: UUID) -> AIJob:
        job = await self.session.get(AIJob, job_id)
        if job is None:
            raise NotFoundError("AI job not found")
        await self.project_service.get_project(job.project_id, owner_id=owner_id)
        return job

    async def list_jobs(self, project_id: UUID, owner_id: UUID) -> list[AIJob]:
        await self.project_service.get_project(project_id, owner_id=owner_id)
        from sqlalchemy import select

        result = await self.session.execute(
            select(AIJob).where(AIJob.project_id == project_id).order_by(AIJob.created_at.desc())
        )
        return list(result.scalars().all())

    async def complete_job(self, job_id: UUID, result: dict) -> AIJob:
        job = await self.session.get(AIJob, job_id)
        if job is None:
            raise NotFoundError("AI job not found")
        job.status = "completed"
        job.result = result
        job.completed_at = datetime.now(UTC)
        await self.session.flush()
        await self.session.refresh(job)
        return job

    async def fail_job(self, job_id: UUID, error: str) -> AIJob:
        job = await self.session.get(AIJob, job_id)
        if job is None:
            raise NotFoundError("AI job not found")
        if job.status not in AI_JOB_STATUSES:
            pass
        job.status = "failed"
        job.error_message = error
        job.completed_at = datetime.now(UTC)
        await self.session.flush()
        await self.session.refresh(job)
        return job
