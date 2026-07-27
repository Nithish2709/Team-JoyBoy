"""
Authentication endpoint tests.
"""
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from httpx import AsyncClient


async def test_register_success(client: AsyncClient):
    """Registration with valid data returns 201 and user object."""
    from app.models.role import RoleName
    mock_role = MagicMock()
    mock_role.id = 1
    mock_role.name = RoleName.SUPER_ADMIN

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@pds.gov.in"
    mock_user.full_name = "Test User"
    mock_user.is_active = True
    mock_user.district_id = None
    mock_user.taluk_id = None
    mock_user.created_at = "2026-01-01T00:00:00"
    mock_user.updated_at = "2026-01-01T00:00:00"
    mock_user.role = mock_role

    with patch("app.services.auth.AuthService.register", return_value=mock_user):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@pds.gov.in",
                "password": "Secure@123",
                "full_name": "Test User",
                "role_id": 1,
            },
        )
    assert response.status_code == 201


async def test_login_success(client: AsyncClient):
    """Valid credentials return token response."""
    from app.schemas.auth import TokenResponse
    mock_token = TokenResponse(
        access_token="mock.jwt.token",
        refresh_token="mock_refresh_token",
        expires_in=1800,
    )
    with patch("app.services.auth.AuthService.login", return_value=mock_token):
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "test@pds.gov.in", "password": "Secure@123"},
        )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_invalid_credentials(client: AsyncClient):
    """Invalid credentials return 401."""
    from fastapi import HTTPException, status
    with patch(
        "app.services.auth.AuthService.login",
        side_effect=HTTPException(status_code=401, detail="Invalid email or password.")
    ):
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "bad@email.com", "password": "wrongpass"},
        )
    assert response.status_code == 401


async def test_refresh_token_success(client: AsyncClient):
    """Valid refresh token returns new token pair."""
    from app.schemas.auth import TokenResponse
    mock_token = TokenResponse(
        access_token="new.jwt.token",
        refresh_token="new_refresh_token",
        expires_in=1800,
    )
    with patch("app.services.auth.AuthService.refresh", return_value=mock_token):
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "valid_refresh_token"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "new.jwt.token"


async def test_logout_success(client: AsyncClient):
    """Logout invalidates refresh token and returns 200."""
    with patch("app.services.auth.AuthService.logout", return_value=None):
        response = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "some_refresh_token"},
        )
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out."


async def test_protected_route_without_token(client: AsyncClient):
    """Accessing a protected route without a token returns 401."""
    response = await client.get("/api/v1/users/")
    assert response.status_code == 401


async def test_protected_route_with_invalid_token(client: AsyncClient):
    """Accessing a protected route with a bad token returns 401."""
    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": "Bearer this.is.invalid"}
    )
    assert response.status_code == 401
