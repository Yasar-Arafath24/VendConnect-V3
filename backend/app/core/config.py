from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =====================================================
    # Application
    # =====================================================
    APP_NAME: str = "VendConnect"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # =====================================================
    # Database (Supabase PostgreSQL)
    # =====================================================
    DATABASE_URL: str = Field(...)

    # =====================================================
    # Supabase
    # =====================================================
    SUPABASE_URL: str = Field(...)
    SUPABASE_ANON_KEY: str = Field(...)
    SUPABASE_SERVICE_ROLE_KEY: str = Field(...)

    # =====================================================
    # JWT Authentication
    # =====================================================
    JWT_SECRET: str = Field(...)
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # =====================================================
    # CORS
    # =====================================================
    CORS_ORIGINS: str = "http://localhost:5173"

    # =====================================================
    # AI (Groq)
    # =====================================================
    GROQ_API_KEY: str = ""

    # =====================================================
    # Razorpay
    # =====================================================
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    # =====================================================
    # Logging
    # =====================================================
    LOG_LEVEL: str = "INFO"

    # =====================================================
    # Environment Settings
    # =====================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()