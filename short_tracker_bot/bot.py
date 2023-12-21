import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from handlers.hello import router


async def main():
    bot = Bot(token=TOKEN)
    memory = MemoryStorage()
    dp = Dispatcher(memory=memory)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())






