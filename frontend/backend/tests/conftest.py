from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import get_async_db
from unittest.mock import AsyncMock


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """
    Returns an async mock representing a SQLAlchemy session.
    scalar() must return exactly 1 (int) to pass the health check's val == 1 guard.
    """
    from unittest.mock import MagicMock
    mock = AsyncMock()
    # Use a plain MagicMock for the result so scalar() is synchronous and returns 1
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    # execute() is awaited by the endpoint, so it must be an async mock
    mock.execute = AsyncMock(return_value=mock_result)
    return mock


@pytest_asyncio.fixture
async def client(mock_db_session: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client fixture wired to the FastAPI app.
    The database session dependency is replaced with a mock.
    """
    # Override DB dependency with mock session
    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    # Clear dependency overrides after each test
    app.dependency_overrides.clear()
