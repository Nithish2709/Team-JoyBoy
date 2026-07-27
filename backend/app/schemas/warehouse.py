"""
Warehouse Pydantic schemas.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class WarehouseCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    district_id: int
    capacity_tons: float | None = Field(default=None, gt=0)
    address: str | None = None

    model_config = {"json_schema_extra": {"example": {
        "name": "Chennai Central Warehouse",
        "district_id": 1,
        "capacity_tons": 5000.0,
        "address": "Port Area, Chennai"
    }}}


class WarehouseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    capacity_tons: float | None = Field(default=None, gt=0)
    address: str | None = None
    is_active: bool | None = None


class WarehouseResponse(BaseModel):
    id: int
    name: str
    district_id: int
    capacity_tons: float | None
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
