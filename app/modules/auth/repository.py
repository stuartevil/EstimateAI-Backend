"""
Auth repository — delegates to UserRepository.

Keeps auth service decoupled from direct SQLAlchemy usage.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.model import User
from app.modules.users.repository import UserRepository


class AuthRepository:
    """Authentication data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repo.get_by_email(email)

    async def create_user(self, user: User) -> User:
        return await self.user_repo.create(user)
