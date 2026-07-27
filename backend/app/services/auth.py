"""
AuthService — registration, login, token refresh, and logout business logic.
"""
import secrets
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.db.redis import redis_manager
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse


REFRESH_TOKEN_PREFIX = "refresh_token:"


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> User:
        """Register a new user after validating email uniqueness."""
        if await self.user_repo.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists."
            )
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role_id=data.role_id,
            district_id=data.district_id,
            taluk_id=data.taluk_id,
        )
        return await self.user_repo.create(user)

    async def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate credentials and return JWT + refresh token pair."""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated."
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = await self._create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Issue new access token using a valid refresh token."""
        user_id = await self._validate_refresh_token(refresh_token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )
        user = await self.user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or deactivated."
            )

        # Rotate: delete old, issue new
        await self._delete_refresh_token(refresh_token)
        new_access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = await self._create_refresh_token(user.id)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def logout(self, refresh_token: str) -> None:
        """Invalidate the refresh token in Redis."""
        await self._delete_refresh_token(refresh_token)

    # --- Internal helpers ---

    async def _create_refresh_token(self, user_id: int) -> str:
        token = secrets.token_urlsafe(48)
        key = f"{REFRESH_TOKEN_PREFIX}{token}"
        expire_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
        client = redis_manager.get_client()
        await client.set(key, str(user_id), ex=expire_seconds)
        return token

    async def _validate_refresh_token(self, token: str) -> str | None:
        key = f"{REFRESH_TOKEN_PREFIX}{token}"
        client = redis_manager.get_client()
        value = await client.get(key)
        return value.decode() if value else None

    async def _delete_refresh_token(self, token: str) -> None:
        key = f"{REFRESH_TOKEN_PREFIX}{token}"
        client = redis_manager.get_client()
        await client.delete(key)
