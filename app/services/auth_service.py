from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import AuthResponse, RegisterRequest
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService
from app.shared.exceptions import UnauthorizedError


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)
        self.user_service = UserService(session)

    async def register(self, data: RegisterRequest) -> AuthResponse:
        user = await self.user_service.create_user(
            UserCreate(name=data.name, email=data.email, password=data.password)
        )
        token = create_access_token(subject=user.id)
        return AuthResponse(access_token=token, user=UserResponse.model_validate(user))

    async def login(self, email: str, password: str) -> AuthResponse:
        user = await self.user_repo.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is inactive")
        token = create_access_token(subject=user.id)
        return AuthResponse(access_token=token, user=UserResponse.model_validate(user))
