import aiohttp


class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(base_url=self.base_url)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


class CryptoClient(BaseClient):
    async def get(self, url: str):
        async with self.session.get(self.base_url + url) as response:
            response = await response.json()
            response = response["result"]
            index_price, instrument_name, timestamp = (
                response["index_price"],
                response["instrument_name"],
                response["timestamp"],
            )
            context = {
                "index_price": index_price,
                "instrument_name": instrument_name,
                "timestamp": timestamp // 1000,
            }
            return context
