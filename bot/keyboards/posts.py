from aiogram.utils.keyboard import InlineKeyboardBuilder


def channels_keyboard(channels):
    builder = InlineKeyboardBuilder()
    for ch in channels:
        builder.button(text=ch.title, callback_data=f"pch:{ch.id}")
    builder.adjust(1)
    return builder.as_markup()


def confirm_keyboard(_):
    builder = InlineKeyboardBuilder()
    builder.button(text=_("post.save"), callback_data="post_save")
    builder.button(text=_("post.cancel"), callback_data="post_cancel")
    builder.adjust(2)
    return builder.as_markup()


def when_keyboard(_):
    builder = InlineKeyboardBuilder()
    builder.button(text=_("post.now"), callback_data="when_now")
    builder.button(text=_("post.later"), callback_data="when_later")
    builder.adjust(2)
    return builder.as_markup()
