import pytest
import aiohttp
import pytest_asyncio

@pytest_asyncio.fixture
async def async_session():
    """Fixture para proporcionar una sesión de aiohttp a los tests asíncronos."""
    async with aiohttp.ClientSession() as session:
        yield session