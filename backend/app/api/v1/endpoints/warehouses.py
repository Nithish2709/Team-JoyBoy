"""
Warehouses router — Warehouse CRUD with RBAC.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_db
from app.core.dependencies import get_current_user, require_roles
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.warehouse import WarehouseService
from app.models.user import User

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])

_WRITE_ROLES = ("super_admin", "state_officer", "district_officer")


@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new Warehouse",
)
async def create_warehouse(
    data: WarehouseCreate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES)),
):
    return await WarehouseService(db).create_warehouse(data)


@router.get(
    "/",
    response_model=PaginatedResponse[WarehouseResponse],
    summary="List warehouses with optional district filter",
)
async def list_warehouses(
    page: int = 1,
    page_size: int = 20,
    district_id: int | None = None,
    active_only: bool = False,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user),
):
    service = WarehouseService(db)
    items, total = await service.list_warehouses(page, page_size, district_id, active_only)
    return PaginatedResponse.build(
        items=[WarehouseResponse.model_validate(w) for w in items],
        total=total, page=page, page_size=page_size
    )


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
    summary="Get a warehouse by ID",
)
async def get_warehouse(
    warehouse_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user),
):
    return await WarehouseService(db).get_warehouse(warehouse_id)


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
    summary="Update a warehouse",
)
async def update_warehouse(
    warehouse_id: int,
    data: WarehouseUpdate,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles(*_WRITE_ROLES)),
):
    return await WarehouseService(db).update_warehouse(warehouse_id, data)


@router.delete(
    "/{warehouse_id}",
    response_model=MessageResponse,
    summary="Delete a warehouse",
)
async def delete_warehouse(
    warehouse_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: User = Depends(require_roles("super_admin", "state_officer")),
):
    await WarehouseService(db).delete_warehouse(warehouse_id)
    return MessageResponse(message="Warehouse deleted successfully.")
