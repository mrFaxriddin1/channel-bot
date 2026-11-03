from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import settings
from bot.services.subscription import is_subscribed

router = Router()


@router.callback_query(F.data == "check_sub")
async def on_check_subscription(callback: CallbackQuery, bot, _):
    if await is_subscribed(bot, settings.required_channel, callback.from_user.id):
        await callback.message.edit_text(  # type: ignore
            _("start.greeting", name=callback.from_user.full_name)
        )
        await callback.answer()
    else:
        await callback.answer(_("sub.still_not"), show_alert=True)
