from aiogram.utils.keyboard import InlineKeyboardBuilder


def subscription_keyboard(channel: str, _):
    builder = InlineKeyboardBuilder()
    url = f"https://t.me/{channel.lstrip('@')}"
    builder.button(text=_("sub.join"), url=url)
    builder.button(text=_("sub.check"), callback_data="check_sub")
    builder.adjust(1)
    return builder.as_markup()
