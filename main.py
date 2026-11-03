import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.database.session import session_maker
from bot.handlers import start, subscription
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.i18n import I18nMiddleware
from bot.middlewares.subscription import SubscriptionMiddleware


async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_maker))
    dp.update.middleware(I18nMiddleware())
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    dp.include_router(start.router)
    dp.include_router(subscription.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
