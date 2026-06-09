"""Authentication request/response schemas."""

from pydantic import BaseModel, EmailStr, Field

from app.modules.users.schema import UserResponse


class RegisterRequest(BaseModel):
    """User registration payload."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """JSON login payload (alternative to OAuth2 form)."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    """Login response with token and user profile."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
