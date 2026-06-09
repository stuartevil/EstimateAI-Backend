"""
Application configuration via Pydantic Settings.

Centralizes environment-driven configuration so infrastructure concerns
remain decoupled from business modules (Clean Architecture boundary).
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root (estimate_ai_backend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Typed settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="EstimateAI", alias="APP_NAME")
    debug: bool = Field(default=False, alias="DEBUG")

    database_url: str = Field(alias="DATABASE_URL")

    secret_key: str = Field(alias="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    upload_dir: Path = Field(default=BASE_DIR / "uploads", alias="UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=50, alias="MAX_UPLOAD_SIZE_MB")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: Path = Field(default=BASE_DIR / "logs" / "estimateai.log", alias="LOG_FILE")

    @field_validator("upload_dir", "log_file", mode="before")
    @classmethod
    def resolve_paths(cls, value: str | Path) -> Path:
        path = Path(value)
        if not path.is_absolute():
            return BASE_DIR / path
        return path

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton for dependency injection."""
    return Settings()
