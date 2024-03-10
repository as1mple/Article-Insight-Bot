import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from modules.handlers import message, button
from settings import TOKEN, LOGCONFIG


async def main():
    logger.configure(
        handlers=LOGCONFIG.to_dicts(),
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)

    logger.info("Bot started.")

    dp.include_router(message.router)
    dp.include_router(button.router)

    logger.info("Routers included.")

    await bot.set_my_commands([
        {"command": "/start", "description": "Start the bot"},
        {"command": "/today_news", "description": "Get today news"},
    ])

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
