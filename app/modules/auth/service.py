"""
Authentication business logic.

Handles registration, login, and token issuance.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schema import AuthResponse, RegisterRequest
from app.modules.users.schema import UserCreate, UserResponse
from app.modules.users.service import UserService
from app.shared.exceptions import UnauthorizedError


class AuthService:
    """Authentication domain service."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = AuthRepository(session)
        self.user_service = UserService(session)

    async def register(self, data: RegisterRequest) -> AuthResponse:
        """Register a new user and return an access token."""
        user = await self.user_service.create_user(
            UserCreate(name=data.name, email=data.email, password=data.password)
        )
        token = create_access_token(subject=user.id)
        return AuthResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    async def login(self, email: str, password: str) -> AuthResponse:
        """Authenticate credentials and return an access token."""
        user = await self.repo.get_user_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is inactive")

        token = create_access_token(subject=user.id)
        return AuthResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )
