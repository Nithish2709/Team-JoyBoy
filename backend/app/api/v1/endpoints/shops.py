"""
Shops router — FairPriceShop CRUD with RBAC.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_db
from app.core.dependencies import get_current_user, require_roles
from app.schemas.shop import ShopCreate, ShopUpdate, ShopResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.shop import ShopService
from app.models.user import User

router = APIRouter(prefix="/shops", tags=["Fair Price Shops"])

_WRITE_ROLES = ("super_admin", "state_officer", "district_officer")


@router.post(
    "/",
    response_model=ShopResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new Fair Price Shop",
)
async def create_shop(
    data: ShopCreate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES, "taluk_officer")),
):
    return await ShopService(db).create_shop(data)


@router.get(
    "/",
    response_model=PaginatedResponse[ShopResponse],
    summary="List shops with optional district/taluk filters",
)
async def list_shops(
    page: int = 1,
    page_size: int = 20,
    district_id: int | None = None,
    taluk_id: int | None = None,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user),
):
    service = ShopService(db)
    items, total = await service.list_shops(page, page_size, district_id, taluk_id)
    return PaginatedResponse.build(
        items=[ShopResponse.model_validate(s) for s in items],
        total=total, page=page, page_size=page_size
    )


@router.get(
    "/{shop_id}",
    response_model=ShopResponse,
    summary="Get a shop by ID",
)
async def get_shop(
    shop_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user),
):
    return await ShopService(db).get_shop(shop_id)


@router.put(
    "/{shop_id}",
    response_model=ShopResponse,
    summary="Update a Fair Price Shop",
)
async def update_shop(
    shop_id: int,
    data: ShopUpdate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES)),
):
    return await ShopService(db).update_shop(shop_id, data)


@router.delete(
    "/{shop_id}",
    response_model=MessageResponse,
    summary="Delete a Fair Price Shop",
)
async def delete_shop(
    shop_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles("super_admin", "state_officer")),
):
    await ShopService(db).delete_shop(shop_id)
    return MessageResponse(message="Shop deleted successfully.")
