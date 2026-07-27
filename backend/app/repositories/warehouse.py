"""
WarehouseRepository — Warehouse queries.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.warehouse import Warehouse


class WarehouseRepository(BaseRepository[Warehouse]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Warehouse, db)

    async def list_by_district(
        self, district_id: int, page: int = 1, page_size: int = 20
    ):
        return await self.paginate(
            page, page_size, [Warehouse.district_id == district_id]
        )

    async def list_active(self, page: int = 1, page_size: int = 20):
        return await self.paginate(
            page, page_size, [Warehouse.is_active == True]  # noqa: E712
        )
