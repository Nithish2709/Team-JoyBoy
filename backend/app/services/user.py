"""
UserService — user management business logic.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_with_role(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return user

    async def list_users(self, page: int = 1, page_size: int = 20) -> tuple[list[User], int]:
        return await self.repo.paginate(page, page_size)

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        if not await self.repo.exists(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        update_data = data.model_dump(exclude_none=True)
        updated = await self.repo.update(user_id, update_data)
        return updated

    async def deactivate_user(self, user_id: int) -> None:
        if not await self.repo.exists(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        await self.repo.update(user_id, {"is_active": False})
