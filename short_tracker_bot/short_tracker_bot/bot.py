import asyncio
import logging
import os

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import COMMANDS
from handlers.hello import router

dotenv.load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    memory = MemoryStorage()
    dp = Dispatcher(memory=memory)
    dp.include_router(router)
    await bot.set_my_commands(commands=COMMANDS)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
