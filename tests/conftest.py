import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import engine
from sqlalchemy import text

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def clean_db():
    yield
    async with AsyncSession(engine) as session:
        await session.execute(text("TRUNCATE users, trips, day_task RESTART IDENTITY CASCADE"))
        await session.commit()