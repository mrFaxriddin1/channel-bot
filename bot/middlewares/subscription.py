from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.config import settings
from bot.keyboards.subscription import subscription_keyboard
from bot.services.subscription import is_subscribed


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        bot = data["bot"]
        _ = data["_"]

        if isinstance(event, CallbackQuery) and event.data == "check_sub":
            return await handler(event, data)

        if await is_subscribed(bot, settings.required_channel, user.id):
            return await handler(event, data)

        text = _("sub.required")
        markup = subscription_keyboard(settings.required_channel, _)
        if isinstance(event, Message):
            await event.answer(text, reply_markup=markup)
        elif isinstance(event, CallbackQuery):
            await event.message.answer(text, reply_markup=markup)  # type: ignore
            await event.answer()
