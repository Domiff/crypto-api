from typing import TYPE_CHECKING

from sqlalchemy import select

from src.crypto.models import CryptoCurrency

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_data(session: AsyncSession, ticker: str) -> Sequence[CryptoCurrency]:
    result = await session.execute(
        select(CryptoCurrency).where(CryptoCurrency.ticker == ticker)
    )
    return result.scalars().all()


async def get_last_price(session: AsyncSession, ticker: str) -> CryptoCurrency | None:
    result = await session.execute(
        select(CryptoCurrency)
        .where(CryptoCurrency.ticker == ticker)
        .order_by(CryptoCurrency.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_ticker_with_date_filter(
    session: AsyncSession,
    ticker: str,
    date_start: datetime,
    date_end: datetime,
) -> Sequence[CryptoCurrency]:
    result = await session.execute(
        select(CryptoCurrency).where(
            CryptoCurrency.ticker == ticker,
            CryptoCurrency.created_at >= date_start,
            CryptoCurrency.created_at <= date_end,
        )
    )
    return result.scalars().all()


async def add_crypto_data(session: AsyncSession, data: dict[str, dict]) -> None:
    session.add_all(
        CryptoCurrency(
            ticker=ticker,
            index_price=item["index_price"],
            instrument_name=item["instrument_name"],
        )
        for ticker, item in data.items()
    )
    await session.commit()
