from functools import partial
from typing import Any
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.i18n import DEFAULT_LANG, t
from bot.repositories import users as users_repo


class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        lang = DEFAULT_LANG
        tg_user = data.get("event_from_user")
        session = data.get("session")

        if tg_user and session:
            user = await users_repo.get_user(session, tg_user.id)
            if user:
                lang = user.language

        data["lang"] = lang
        data["_"] = partial(t, lang=lang)
        return await handler(event, data)
