"""
FastAPI dependency injection: current user resolution and RBAC enforcement.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_access_token
from app.db.database import get_async_db

# OAuth2 scheme — token is taken from Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    """
    Dependency: Decode JWT, load user from DB, verify is_active.
    Import User model lazily to avoid circular imports.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Lazy import to prevent circular dependency
    from app.repositories.user import UserRepository
    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated."
        )
    return user


def require_roles(*allowed_roles: str):
    """
    Dependency factory: enforce that the current user's role is in allowed_roles.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_roles("super_admin"))])
    """
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {list(allowed_roles)}"
            )
        return current_user
    return role_checker
