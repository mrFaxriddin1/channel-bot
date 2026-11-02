from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.i18n import t
from bot.keyboards.language import language_keyboard
from bot.repositories import users as users_repo

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, _):
    if message.from_user is None:
        return

    user = await users_repo.get_user(session, message.from_user.id)
    if user is None:
        await users_repo.create_user(session, message.from_user.id, "uz")
        await message.answer(_("language.choose"), reply_markup=language_keyboard())
        return
    await message.answer(_("start.greeting", name=message.from_user.full_name))


@router.message(Command("language"))
async def cmd_language(message: Message, _):
    await message.answer(_("language.choose"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def on_language_chosen(callback: CallbackQuery, session: AsyncSession):
    if callback.data is None:
        return

    lang = callback.data.split(":")[1]
    await users_repo.set_language(session, callback.from_user.id, lang)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(t("language.changed", lang))

    await callback.answer()
