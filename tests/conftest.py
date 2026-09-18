from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.core.models import Base
from src.crypto.models import CryptoCurrency


@pytest.fixture
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
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
                CryptoCurrency(
                    ticker="btc",
                    index_price=90_000.0,
                    instrument_name="btc_usd",
                    created_at=datetime(2026, 1, 17, 12, tzinfo=UTC),
                ),
                CryptoCurrency(
                    ticker="btc",
                    index_price=100_000.0,
                    instrument_name="btc_usd",
                    created_at=datetime(2026, 1, 18, 12, tzinfo=UTC),
                ),
                CryptoCurrency(
                    ticker="eth",
                    index_price=4_000.0,
                    instrument_name="eth_usd",
                    created_at=datetime(2026, 1, 18, 12, tzinfo=UTC),
                ),
            ]
        )
        await session.commit()
        yield session


@pytest.fixture
def start():
    return datetime(2026, 1, 18, tzinfo=UTC)


@pytest.fixture
def end():
    return datetime(2026, 1, 19, tzinfo=UTC)
