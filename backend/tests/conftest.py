"""
Global pytest fixtures for PDS Sentinel AI test suite.
"""
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.db.database import get_async_db


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """
    Returns an async mock representing a SQLAlchemy session.
    scalar() must return exactly 1 (int) to pass the health check's val == 1 guard.
    """
    mock = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    mock.execute = AsyncMock(return_value=mock_result)
    return mock


@pytest_asyncio.fixture
async def client(mock_db_session: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client fixture wired to the FastAPI app.
    The database session dependency is replaced with a mock for health tests.
    """
    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def raw_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client without any dependency overrides.
    Used by tests that manage their own mocking via patch().
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
