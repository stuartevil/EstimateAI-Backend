from uuid import UUID

from loguru import logger


class TaskQueue:
    """In-process task queue placeholder — replace with Celery/Redis in production."""

    async def enqueue(self, job_id: UUID, job_type: str) -> None:
        logger.info("Enqueued job {} of type {}", job_id, job_type)
