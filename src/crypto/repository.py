from typing import TYPE_CHECKING, Sequence

from sqlalchemy import select

from src.crypto.models import Btc, Eth

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


CryptoType = Sequence[Btc | Eth]


async def get_all_data(session: "AsyncSession", ticker: str) -> CryptoType:
    if ticker == "btc":
        result = await session.execute(select(Btc))
        return result.scalars().all()
    elif ticker == "eth":
        result = await session.execute(select(Eth))
        return result.scalars().all()
    raise ValueError(f"Unknown ticker: {ticker}")


async def get_last_price(session: "AsyncSession", ticker: str) -> Btc | Eth | None:
    if ticker == "btc":
        result = await session.execute(select(Btc).order_by(Btc.id.desc()).limit(1))
        return result.scalar_one_or_none()
    elif ticker == "eth":
        result = await session.execute(select(Eth).order_by(Eth.id.desc()).limit(1))
        return result.scalar_one_or_none()
    raise ValueError(f"Unknown ticker: {ticker}")


async def get_ticker_with_date_filter(
    session: "AsyncSession",
    ticker: str,
    date_start: "datetime",
    date_end: "datetime",
) -> CryptoType:
    start_ts = date_start.timestamp()
    end_ts = date_end.timestamp()

    if ticker == "btc":
        result = await session.execute(
            select(Btc).where(Btc.timestamp >= start_ts, Btc.timestamp <= end_ts)
        )
        return result.scalars().all()
    elif ticker == "eth":
        result = await session.execute(
            select(Eth).where(Eth.timestamp >= start_ts, Eth.timestamp <= end_ts)
        )
        return result.scalars().all()
    raise ValueError(f"Unknown ticker: {ticker}")


async def add_crypto_data(
    btc_data: dict,
    eth_data: dict,
    session: "async_sessionmaker[AsyncSession]",
) -> None:
    async with session() as s:
        s.add(Btc(
            index_price=btc_data["index_price"],
            instrument_name=btc_data["instrument_name"],
            timestamp=btc_data["timestamp"],
        ))
        s.add(Eth(
            index_price=eth_data["index_price"],
            instrument_name=eth_data["instrument_name"],
            timestamp=eth_data["timestamp"],
        ))
        await s.commit()
