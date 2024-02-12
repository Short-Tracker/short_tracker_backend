import logging

import aiohttp


async def request_get(url, headers=None):
    logging.info(f'request func {url}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            logging.info(response)
            data = await response.json()
            logging.info(data)
            return data


async def request_post(url, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            return response
