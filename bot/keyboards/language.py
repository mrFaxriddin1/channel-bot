from aiogram.utils.keyboard import InlineKeyboardBuilder

LANG_NAMES = {"uz": "🇺🇿 O'zbekcha", "en": "🇬🇧 English", "ru": "🇷🇺 Русский"}


def language_keyboard():
    builder = InlineKeyboardBuilder()
    for code, name in LANG_NAMES.items():
        builder.button(text=name, callback_data=f"lang:{code}")
    builder.adjust(1)
    return builder.as_markup()
