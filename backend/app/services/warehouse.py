"""
WarehouseService — Warehouse business logic.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.warehouse import Warehouse
from app.repositories.warehouse import WarehouseRepository
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


class WarehouseService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = WarehouseRepository(db)

    async def create_warehouse(self, data: WarehouseCreate) -> Warehouse:
        warehouse = Warehouse(**data.model_dump())
        return await self.repo.create(warehouse)

    async def get_warehouse(self, warehouse_id: int) -> Warehouse:
        warehouse = await self.repo.get_by_id(warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found.")
        return warehouse

    async def list_warehouses(
        self,
        page: int = 1,
        page_size: int = 20,
        district_id: int | None = None,
        active_only: bool = False,
    ) -> tuple[list[Warehouse], int]:
        filters = []
        if district_id:
            filters.append(Warehouse.district_id == district_id)
        if active_only:
            filters.append(Warehouse.is_active == True)  # noqa: E712
        return await self.repo.paginate(page, page_size, filters or None)

    async def update_warehouse(self, warehouse_id: int, data: WarehouseUpdate) -> Warehouse:
        if not await self.repo.exists(warehouse_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found.")
        return await self.repo.update(warehouse_id, data.model_dump(exclude_none=True))

    async def delete_warehouse(self, warehouse_id: int) -> None:
        if not await self.repo.delete(warehouse_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found.")
