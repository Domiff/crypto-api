import aiohttp


class CryptoClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(base_url=self.base_url)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
    
    async def get(self, url: str) -> dict:
        async with self.session.get(self.base_url + url) as response:
            data = await response.json()
            result = data["result"]
            return {
                "index_price": result["index_price"],
                "instrument_name": result["instrument_name"],
                "timestamp": result["timestamp"] // 1000,
            }
