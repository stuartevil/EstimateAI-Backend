from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import AuthService
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/register", response_model=APIResponse[AuthResponse], status_code=201)
async def register(payload: RegisterRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    result = await service.register(payload)
    return success_response(data=result, message="Registration successful")


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
) -> dict:
    result = await service.login(email=form_data.username, password=form_data.password)
    return success_response(data=TokenResponse(access_token=result.access_token), message="Login successful")


@router.post("/login/json", response_model=APIResponse[AuthResponse])
async def login_json(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    result = await service.login(email=payload.email, password=payload.password)
    return success_response(data=result, message="Login successful")
