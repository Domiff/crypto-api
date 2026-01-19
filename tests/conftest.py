from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings.config import settings


@pytest.fixture
async def async_engine():
    engine = create_async_engine(settings.database.db_url, echo=True)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(async_engine):
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
def start():
    return datetime(2026, 1, 18)


@pytest.fixture
def end():
    return datetime(2026, 1, 19)
