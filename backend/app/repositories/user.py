"""
UserRepository — user-specific async queries extending BaseRepository.
"""
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by their email address with role loaded."""
        result = await self.db.execute(
            select(User)
            .where(User.email == email)
            .options(selectinload(User.role))
        )
        return result.scalar_one_or_none()

    async def get_with_role(self, user_id: int) -> User | None:
        """Fetch a user by ID with role eagerly loaded."""
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.role))
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """Check if an email is already registered."""
        result = await self.db.execute(
            select(User.id).where(User.email == email)
        )
        return result.scalar_one_or_none() is not None
