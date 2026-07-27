"""
ShopRepository — FairPriceShop queries.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.shop import FairPriceShop


class ShopRepository(BaseRepository[FairPriceShop]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(FairPriceShop, db)

    async def get_by_shop_number(self, shop_number: str) -> FairPriceShop | None:
        result = await self.db.execute(
            select(FairPriceShop).where(FairPriceShop.shop_number == shop_number)
        )
        return result.scalar_one_or_none()

    async def shop_number_exists(self, shop_number: str) -> bool:
        result = await self.db.execute(
            select(FairPriceShop.id).where(FairPriceShop.shop_number == shop_number)
        )
        return result.scalar_one_or_none() is not None

    async def list_by_district(
        self, district_id: int, page: int = 1, page_size: int = 20
    ):
        return await self.paginate(
            page, page_size, [FairPriceShop.district_id == district_id]
        )

    async def list_by_taluk(
        self, taluk_id: int, page: int = 1, page_size: int = 20
    ):
        return await self.paginate(
            page, page_size, [FairPriceShop.taluk_id == taluk_id]
        )
