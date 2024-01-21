import aiohttp


async def request_get(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data


async def request_post(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return response
