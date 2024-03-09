import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from modules.handlers import message, button
from modules.settings import TOKEN


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)

    dp.include_router(message.router)
    dp.include_router(button.router)

    await bot.set_my_commands([
        {"command": "/start", "description": "Start the bot"},
        {"command": "/today_news", "description": "Get today news"},
    ])

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
