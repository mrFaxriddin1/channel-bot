import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.handlers import start


async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(start.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
