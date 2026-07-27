"""
DistrictRepository and TalukRepository.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.district import District, Taluk


class DistrictRepository(BaseRepository[District]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(District, db)

    async def get_by_code(self, code: str) -> District | None:
        result = await self.db.execute(select(District).where(District.code == code))
        return result.scalar_one_or_none()

    async def code_exists(self, code: str) -> bool:
        result = await self.db.execute(select(District.id).where(District.code == code))
        return result.scalar_one_or_none() is not None

    async def search_by_name(self, name: str, page: int = 1, page_size: int = 20):
        filters = [District.name.ilike(f"%{name}%")]
        return await self.paginate(page, page_size, filters)


class TalukRepository(BaseRepository[Taluk]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Taluk, db)

    async def get_by_district(self, district_id: int) -> list[Taluk]:
        result = await self.db.execute(
            select(Taluk).where(Taluk.district_id == district_id)
        )
        return list(result.scalars().all())

    async def code_exists(self, code: str) -> bool:
        result = await self.db.execute(select(Taluk.id).where(Taluk.code == code))
        return result.scalar_one_or_none() is not None
