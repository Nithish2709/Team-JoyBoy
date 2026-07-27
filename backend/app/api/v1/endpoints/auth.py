"""
Authentication router: register, login, refresh, logout.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_db
from app.schemas.auth import RegisterRequest, TokenResponse, RefreshRequest, LogoutRequest
from app.schemas.user import UserResponse
from app.schemas.common import MessageResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new platform user with the specified role and geographic assignment.",
)
async def register(
    data: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    service = AuthService(db)
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and obtain JWT tokens",
    description="Authenticate with email and password. Returns JWT access token + refresh token.",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    service = AuthService(db)
    return await service.login(form_data.username, form_data.password)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new access + refresh token pair (rotation).",
)
async def refresh_token(
    data: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    service = AuthService(db)
    return await service.refresh(data.refresh_token)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout and invalidate refresh token",
)
async def logout(
    data: LogoutRequest,
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    service = AuthService(db)
    await service.logout(data.refresh_token)
    return MessageResponse(message="Successfully logged out.")
