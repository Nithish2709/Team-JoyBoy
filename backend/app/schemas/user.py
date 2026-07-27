"""
User Pydantic schemas.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.role import RoleName


class RoleResponse(BaseModel):
    id: int
    name: RoleName
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2, max_length=200)
    role_id: int
    district_id: int | None = None
    taluk_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=200)
    district_id: int | None = None
    taluk_id: int | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    role: RoleResponse
    district_id: int | None
    taluk_id: int | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
