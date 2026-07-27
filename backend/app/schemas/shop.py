"""
FairPriceShop Pydantic schemas.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class ShopCreate(BaseModel):
    shop_number: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=2, max_length=200)
    owner_name: str = Field(..., min_length=2, max_length=150)
    address: str | None = None
    district_id: int
    taluk_id: int

    model_config = {"json_schema_extra": {"example": {
        "shop_number": "TN-CHN-001",
        "name": "Anna Nagar FPS",
        "owner_name": "Rajan Kumar",
        "address": "12, Anna Nagar, Chennai",
        "district_id": 1,
        "taluk_id": 1
    }}}


class ShopUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    owner_name: str | None = Field(default=None, min_length=2, max_length=150)
    address: str | None = None
    is_active: bool | None = None


class ShopResponse(BaseModel):
    id: int
    shop_number: str
    name: str
    owner_name: str
    address: str | None
    district_id: int
    taluk_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
