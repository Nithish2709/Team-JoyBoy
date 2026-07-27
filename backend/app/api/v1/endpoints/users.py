"""
Users router — user management with RBAC.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_db
from app.core.dependencies import get_current_user, require_roles
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.user import UserService
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

_ADMINS = ("super_admin", "state_officer")


@router.get(
    "/",
    response_model=PaginatedResponse[UserResponse],
    summary="List all users",
    description="Returns paginated user list. Accessible by Super Admin and State Officer only.",
)
async def list_users(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_ADMINS)),
):
    service = UserService(db)
    items, total = await service.list_users(page, page_size)
    return PaginatedResponse.build(
        items=[UserResponse.model_validate(u) for u in items],
        total=total, page=page, page_size=page_size
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a user by ID",
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_ADMINS)),
):
    service = UserService(db)
    return await service.get_user(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_ADMINS)),
):
    service = UserService(db)
    return await service.update_user(user_id, data)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a user",
    description="Soft-deactivates a user. Super Admin only.",
)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles("super_admin")),
):
    service = UserService(db)
    await service.deactivate_user(user_id)
    return MessageResponse(message="User deactivated successfully.")
