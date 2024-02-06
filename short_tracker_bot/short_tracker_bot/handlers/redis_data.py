import asyncio
import logging

import aioredis

redis = aioredis.Redis(host='redis')


async def save_data_to_redis(key, value):
    logging.info(f'Сохранение в redis {key, value}')
    await redis.set(key, value)


async def get_data_from_redis(key):
    data = await redis.get(key)
    logging.info(f'get data {data}')
    return data
