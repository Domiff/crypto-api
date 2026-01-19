import typing

from fastapi import APIRouter

from src.api.service import get_all_data, get_last_price, get_ticker_with_date_filter

router = APIRouter(tags=["Crypto"])


if typing.TYPE_CHECKING:
    from src.api.annotations import date, ticker_query
    from src.database.connection import SessionDep


@router.get("/crypto")
async def all_data(session: SessionDep, ticker: ticker_query):
    """
    Get all cryptocurrency
    """
    data = await get_all_data(session, ticker)
    return data


@router.get("/last-price")
async def last_price(session: SessionDep, ticker: ticker_query):
    """
    Get last price for cryptocurrency
    """
    data = await get_last_price(session, ticker)
    return data


@router.get("/date-filter")
async def ticker_with_date_filter(
    session: SessionDep, ticker: ticker_query, start_date: date, end_date: date
):
    """
    Get all cryptocurrency with date filter
    """
    data = await get_ticker_with_date_filter(session, ticker, start_date, end_date)
    return data
