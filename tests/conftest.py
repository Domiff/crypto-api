from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.models import Base, Btc, Eth


@pytest.fixture
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///./crypto_test.db", echo=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(async_engine):
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        session.add_all(
            [
                Btc(
                    index_price=100_000.0,
                    instrument_name="BTC_USD",
                    timestamp=1_768_708_800,
                ),
                Eth(
                    index_price=4_000.0,
                    instrument_name="ETH_USD",
                    timestamp=1_768_708_800,
                ),
            ]
        )
        await session.commit()
        yield session


@pytest.fixture
def start():
    return datetime(2026, 1, 18)


@pytest.fixture
def end():
    return datetime(2026, 1, 19)
