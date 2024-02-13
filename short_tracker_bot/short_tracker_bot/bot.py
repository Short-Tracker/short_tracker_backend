import asyncio
import logging
import os

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis
from config import COMMANDS
from handlers.fsm import router

dotenv.load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    redis = aioredis.Redis(host='redis')
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await bot.set_my_commands(commands=COMMANDS)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
