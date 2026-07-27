"""
Districts router — full CRUD with RBAC.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_db
from app.core.dependencies import get_current_user, require_roles
from app.schemas.district import DistrictCreate, DistrictUpdate, DistrictResponse, TalukCreate, TalukResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.district import DistrictService
from app.models.user import User

router = APIRouter(prefix="/districts", tags=["Districts"])

_WRITE_ROLES = ("super_admin", "state_officer")


@router.post(
    "/",
    response_model=DistrictResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new district",
)
async def create_district(
    data: DistrictCreate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES)),
):
    return await DistrictService(db).create_district(data)


@router.get(
    "/",
    response_model=PaginatedResponse[DistrictResponse],
    summary="List districts with optional name filter and pagination",
)
async def list_districts(
    page: int = 1,
    page_size: int = 20,
    name: str | None = None,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user),
):
    service = DistrictService(db)
    items, total = await service.list_districts(page, page_size, name)
    return PaginatedResponse.build(
        items=[DistrictResponse.model_validate(d) for d in items],
        total=total, page=page, page_size=page_size
    )


@router.get(
    "/{district_id}",
    response_model=DistrictResponse,
    summary="Get a district by ID",
)
async def get_district(
    district_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user),
):
    return await DistrictService(db).get_district(district_id)


@router.put(
    "/{district_id}",
    response_model=DistrictResponse,
    summary="Update a district",
)
async def update_district(
    district_id: int,
    data: DistrictUpdate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES)),
):
    return await DistrictService(db).update_district(district_id, data)


@router.delete(
    "/{district_id}",
    response_model=MessageResponse,
    summary="Delete a district",
)
async def delete_district(
    district_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles("super_admin")),
):
    await DistrictService(db).delete_district(district_id)
    return MessageResponse(message="District deleted successfully.")


@router.post(
    "/{district_id}/taluks",
    response_model=TalukResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a taluk to a district",
)
async def create_taluk(
    district_id: int,
    data: TalukCreate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES)),
):
    data.district_id = district_id
    return await DistrictService(db).create_taluk(data)
