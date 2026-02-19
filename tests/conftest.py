import pytest
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async httpx AsyncClient fixture using ASGITransport.

    Requires `pytest-asyncio` (dev dependency). Tests that use this fixture
    should be declared `async def` and marked with `@pytest.mark.asyncio`.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
