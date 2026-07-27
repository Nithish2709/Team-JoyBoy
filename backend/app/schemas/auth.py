"""
Auth Pydantic schemas: request/response models for authentication endpoints.
"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    full_name: str = Field(..., min_length=2, max_length=200)
    role_id: int = Field(..., description="Role ID to assign to the user")
    district_id: int | None = Field(default=None, description="Optional district assignment")
    taluk_id: int | None = Field(default=None, description="Optional taluk assignment")

    model_config = {"json_schema_extra": {"example": {
        "email": "officer@pds.gov.in",
        "password": "Secure@123",
        "full_name": "District Officer Tamil Nadu",
        "role_id": 3,
        "district_id": 1
    }}}


class LoginRequest(BaseModel):
    username: str = Field(..., description="User email address")
    password: str = Field(..., description="Account password")

    model_config = {"json_schema_extra": {"example": {
        "username": "officer@pds.gov.in",
        "password": "Secure@123"
    }}}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token expiry in seconds")


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid refresh token")


class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token to invalidate")
