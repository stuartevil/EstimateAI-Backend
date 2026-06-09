"""Auth data access — delegates to UserRepository."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.service.user_repository import UserRepository


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repo.get_by_email(email)

    async def create_user(self, user: User) -> User:
        return await self.user_repo.create(user)
