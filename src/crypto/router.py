from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query, status

from src.core.database import SessionDep
from src.crypto.repository import get_all_data, get_last_price, get_ticker_with_date_filter

router = APIRouter(tags=["Crypto"])

TickerQuery = Annotated[Literal["btc", "eth"], Query()]
DateQuery = Annotated[datetime, Query()]


@router.get("/crypto")
async def all_data(session: SessionDep, ticker: TickerQuery):
    return await get_all_data(session, ticker)


@router.get("/last-price")
async def last_price(session: SessionDep, ticker: TickerQuery):
    data = await get_last_price(session, ticker)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data for the specified currency",
        )
    return data


@router.get("/date-filter")
async def ticker_with_date_filter(
    session: SessionDep,
    ticker: TickerQuery,
    start_date: DateQuery,
    end_date: DateQuery,
):
    return await get_ticker_with_date_filter(session, ticker, start_date, end_date)
