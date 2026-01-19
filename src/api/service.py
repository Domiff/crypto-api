import typing

from fastapi import HTTPException, status
from sqlalchemy import select

from src.database.models import Btc, Eth

if typing.TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_data(session: AsyncSession, ticker: str):
    if ticker == "btc":
        query = select(Btc)
        btc = await session.execute(query)
        return btc.scalars().all()
    elif ticker == "eth":
        query = select(Eth)
        eth = await session.execute(query)
        return eth.scalars().all()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The specified currency is not in the database",
    )


async def get_last_price(session: AsyncSession, ticker: str):
    if ticker == "btc":
        query = select(Btc).order_by(Btc.id.desc()).limit(1)
        btc = await session.execute(query)
        return btc.scalar_one_or_none()
    elif ticker == "eth":
        query = select(Eth).order_by(Eth.id.desc()).limit(1)
        eth = await session.execute(query)
        return eth.scalar_one_or_none()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The specified currency is not in the database",
    )


async def get_ticker_with_date_filter(
    session: AsyncSession, ticker: str, date_start: datetime, date_end: datetime
):
    start_timestamp = date_start.timestamp()
    end_timestamp = date_end.timestamp()

    if ticker == "btc":
        query = select(Btc).where(
            Btc.timestamp >= start_timestamp, Btc.timestamp <= end_timestamp
        )
        btc = await session.execute(query)
        btc = await session.execute(query)
        return btc.scalars().all()
    elif ticker == "eth":
        query = select(Eth).where(
            Eth.timestamp >= start_timestamp, Eth.timestamp <= end_timestamp
        )
        eth = await session.execute(query)
        return eth.scalars().all()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The specified currency is not in the database",
    )
