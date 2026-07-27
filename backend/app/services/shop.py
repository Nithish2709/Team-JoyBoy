"""
ShopService — FairPriceShop business logic.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.shop import FairPriceShop
from app.repositories.shop import ShopRepository
from app.schemas.shop import ShopCreate, ShopUpdate


class ShopService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = ShopRepository(db)

    async def create_shop(self, data: ShopCreate) -> FairPriceShop:
        if await self.repo.shop_number_exists(data.shop_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Shop with number '{data.shop_number}' already exists."
            )
        shop = FairPriceShop(**data.model_dump())
        return await self.repo.create(shop)

    async def get_shop(self, shop_id: int) -> FairPriceShop:
        shop = await self.repo.get_by_id(shop_id)
        if not shop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found.")
        return shop

    async def list_shops(
        self,
        page: int = 1,
        page_size: int = 20,
        district_id: int | None = None,
        taluk_id: int | None = None,
    ) -> tuple[list[FairPriceShop], int]:
        filters = []
        if district_id:
            filters.append(FairPriceShop.district_id == district_id)
        if taluk_id:
            filters.append(FairPriceShop.taluk_id == taluk_id)
        return await self.repo.paginate(page, page_size, filters or None)

    async def update_shop(self, shop_id: int, data: ShopUpdate) -> FairPriceShop:
        if not await self.repo.exists(shop_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found.")
        return await self.repo.update(shop_id, data.model_dump(exclude_none=True))

    async def delete_shop(self, shop_id: int) -> None:
        if not await self.repo.delete(shop_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found.")
