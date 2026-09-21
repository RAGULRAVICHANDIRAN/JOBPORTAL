"""
JobPilot AI — Backend Application Configuration

Loads settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    app_name: str = "JobPilot AI"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-this-to-a-random-secret-key"

    # Database
    database_url: str = "sqlite+aiosqlite:///./jobpilot.db"

    # Redis
    redis_url: Optional[str] = None

    # JWT
    jwt_secret_key: str = "change-this-to-a-random-jwt-secret"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    jwt_algorithm: str = "HS256"

    # AI Provider
    ai_provider: str = "mock"  # openai | gemini | mock
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None

    # Email
    email_provider: str = "mock"  # smtp | sendgrid | mock
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    sendgrid_api_key: Optional[str] = None

    # Push Notifications
    push_notification_key: Optional[str] = None

    # Rate Limits
    rate_limit_per_minute: int = 60
    max_applications_per_day: int = 30

    # File Upload
    max_upload_size_mb: int = 10
    upload_dir: str = "./uploads"

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Locale
    default_currency: str = "INR"
    default_locale: str = "en-IN"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — loaded once per process."""
    return Settings()
