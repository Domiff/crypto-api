from src.crypto.repository import (
    add_crypto_data,
    get_all_data,
    get_last_price,
    get_ticker_with_date_filter,
)


async def test_get_all_data(session):
    data_btc = await get_all_data(session, "btc")
    data_eth = await get_all_data(session, "eth")
    assert len(data_btc) == 2
    assert len(data_eth) == 1
    assert all(item.ticker == "btc" for item in data_btc)
    assert all(item.ticker == "eth" for item in data_eth)


async def test_get_all_data_unknown_ticker(session):
    assert await get_all_data(session, "sol") == []


async def test_get_last_price(session):
    data_btc = await get_last_price(session, "btc")
    data_eth = await get_last_price(session, "eth")
    assert data_btc is not None
    assert data_eth is not None
    assert data_btc.index_price == 100_000.0
    assert data_eth.index_price == 4_000.0


async def test_get_last_price_unknown_ticker(session):
    assert await get_last_price(session, "sol") is None


async def test_get_ticker_with_date_filter(session, start, end):
    data_btc = await get_ticker_with_date_filter(session, "btc", start, end)
    data_eth = await get_ticker_with_date_filter(session, "eth", start, end)
    assert [item.index_price for item in data_btc] == [100_000.0]
    assert [item.index_price for item in data_eth] == [4_000.0]


async def test_add_crypto_data(session):
    await add_crypto_data(
        session,
        {
            "btc": {"index_price": 110_000.0, "instrument_name": "btc_usd"},
            "sol": {"index_price": 200.0, "instrument_name": "sol_usd"},
        },
    )
    data_btc = await get_all_data(session, "btc")
    data_sol = await get_all_data(session, "sol")
    assert len(data_btc) == 3
    assert len(data_sol) == 1
    assert data_sol[0].created_at is not None
