from src.core.models import Btc, Eth
from src.crypto.repository import get_all_data, get_last_price, get_ticker_with_date_filter


async def test_get_all_data(session):
    data_btc = await get_all_data(session, "btc")
    data_eth = await get_all_data(session, "eth")
    assert data_btc is not None
    assert data_eth is not None
    assert isinstance(data_btc, list)
    assert isinstance(data_eth, list)


async def test_get_last_price(session):
    data_btc = await get_last_price(session, "btc")
    data_eth = await get_last_price(session, "eth")
    assert data_btc is not None
    assert data_eth is not None
    assert isinstance(data_btc, Btc)
    assert isinstance(data_eth, Eth)


async def test_get_ticker_with_date_filter(session, start, end):
    data_btc = await get_ticker_with_date_filter(session, "btc", start, end)
    data_eth = await get_ticker_with_date_filter(session, "eth", start, end)
    assert data_btc is not None
    assert data_eth is not None
    assert isinstance(data_btc, list)
    assert isinstance(data_eth, list)
