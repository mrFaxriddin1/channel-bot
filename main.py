import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.database.session import session_maker
from bot.handlers import start
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.i18n import I18nMiddleware


async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_maker))
    dp.update.middleware(I18nMiddleware())
    dp.include_router(start.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
