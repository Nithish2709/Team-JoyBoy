"""
District and Taluk Pydantic schemas.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class TalukResponse(BaseModel):
    id: int
    name: str
    code: str
    is_active: bool
    model_config = {"from_attributes": True}


class DistrictCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    state: str = Field(default="Tamil Nadu", max_length=100)
    code: str = Field(..., min_length=2, max_length=20)

    model_config = {"json_schema_extra": {"example": {
        "name": "Chennai", "state": "Tamil Nadu", "code": "CHN"
    }}}


class DistrictUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    is_active: bool | None = None


class DistrictResponse(BaseModel):
    id: int
    name: str
    state: str
    code: str
    is_active: bool
    taluks: list[TalukResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class TalukCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    district_id: int
    code: str = Field(..., min_length=2, max_length=20)


class TalukUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None
