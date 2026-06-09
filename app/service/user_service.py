"""User business logic."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.schema.user import UserCreate, UserUpdate
from app.service.user_repository import UserRepository
from app.utils.exceptions import ConflictError, NotFoundError


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def get_user(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repo.get_by_email(email)

    async def create_user(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ConflictError("Email already registered")

        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        return await self.repo.create(user)

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self.get_user(user_id)

        if data.email and data.email != user.email:
            existing = await self.repo.get_by_email(data.email)
            if existing:
                raise ConflictError("Email already in use")
            user.email = data.email

        if data.name is not None:
            user.name = data.name
        if data.is_active is not None:
            user.is_active = data.is_active

        return await self.repo.update(user)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repo.list_all(skip=skip, limit=limit)
