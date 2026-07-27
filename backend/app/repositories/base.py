"""
Generic async BaseRepository providing reusable CRUD operations for any SQLAlchemy model.
"""
from typing import Any, Generic, TypeVar
from sqlalchemy import select, func, update as sql_update, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """
    Generic async repository. All domain repositories inherit from this class.
    """

    def __init__(self, model: type[ModelT], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    async def get_by_id(self, record_id: int) -> ModelT | None:
        """Fetch a single record by primary key."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == record_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        """Fetch all records with optional pagination."""
        result = await self.db.execute(
            select(self.model).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        """Return total record count."""
        result = await self.db.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def create(self, obj: ModelT) -> ModelT:
        """Persist a new model instance."""
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, record_id: int, data: dict[str, Any]) -> ModelT | None:
        """Update fields of an existing record by ID."""
        await self.db.execute(
            sql_update(self.model)
            .where(self.model.id == record_id)
            .values(**data)
        )
        await self.db.commit()
        return await self.get_by_id(record_id)

    async def delete(self, record_id: int) -> bool:
        """Hard-delete a record. Returns True if deleted."""
        result = await self.db.execute(
            sql_delete(self.model).where(self.model.id == record_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def exists(self, record_id: int) -> bool:
        """Check if a record with the given ID exists."""
        result = await self.db.execute(
            select(func.count()).select_from(self.model).where(self.model.id == record_id)
        )
        return result.scalar_one() > 0

    async def paginate(
        self, page: int = 1, page_size: int = 20, filters: list | None = None
    ) -> tuple[list[ModelT], int]:
        """
        Return paginated results and total count.
        Returns: (items, total)
        """
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        if filters:
            for f in filters:
                query = query.where(f)
                count_query = count_query.where(f)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        offset = (page - 1) * page_size
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())

        return items, total
