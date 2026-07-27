"""
DistrictService — district and taluk business logic.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.district import District, Taluk
from app.repositories.district import DistrictRepository, TalukRepository
from app.schemas.district import DistrictCreate, DistrictUpdate, TalukCreate


class DistrictService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = DistrictRepository(db)
        self.taluk_repo = TalukRepository(db)

    async def create_district(self, data: DistrictCreate) -> District:
        if await self.repo.code_exists(data.code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"District with code '{data.code}' already exists."
            )
        district = District(**data.model_dump())
        return await self.repo.create(district)

    async def get_district(self, district_id: int) -> District:
        district = await self.repo.get_by_id(district_id)
        if not district:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found.")
        return district

    async def list_districts(
        self, page: int = 1, page_size: int = 20, name: str | None = None
    ) -> tuple[list[District], int]:
        if name:
            return await self.repo.search_by_name(name, page, page_size)
        return await self.repo.paginate(page, page_size)

    async def update_district(self, district_id: int, data: DistrictUpdate) -> District:
        if not await self.repo.exists(district_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found.")
        return await self.repo.update(district_id, data.model_dump(exclude_none=True))

    async def delete_district(self, district_id: int) -> None:
        if not await self.repo.delete(district_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found.")

    async def create_taluk(self, data: TalukCreate) -> Taluk:
        if not await self.repo.exists(data.district_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found.")
        if await self.taluk_repo.code_exists(data.code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Taluk with code '{data.code}' already exists."
            )
        taluk = Taluk(**data.model_dump())
        return await self.taluk_repo.create(taluk)
