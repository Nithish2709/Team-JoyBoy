import os
from typing import Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # --- Application ---
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    DEBUG: bool = True
    PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "replace_this_with_a_secure_cryptographic_random_key_64_bytes_long"

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://pds_user:pds_password@db:5432/pds_sentinel_db"

    # --- Redis ---
    REDIS_URL: str = "redis://redis:6379/0"

    # --- JWT ---
    JWT_SECRET_KEY: str = "replace_this_with_a_jwt_secret_key_64_bytes_minimum_length_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://") and not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL connection string")
        if v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("REDIS_URL")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        if not v.startswith("redis://") and not v.startswith("rediss://"):
            raise ValueError("REDIS_URL must start with redis:// or rediss://")
        return v


# Instantiate settings singleton
settings = Settings()
