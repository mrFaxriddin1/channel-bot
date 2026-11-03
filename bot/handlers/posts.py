from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import IsAdmin
from bot.keyboards.posts import channels_keyboard, confirm_keyboard
from bot.repositories import channels as channels_repo
from bot.repositories import posts as posts_repo

router = Router()


class NewPost(StatesGroup):
    choosing_channel = State()
    waiting_content = State()
    confirming = State()


@router.message(Command("newpost"), IsAdmin())
async def cmd_new_post(message: Message, state: FSMContext, session: AsyncSession, _):
    channels = await channels_repo.get_channels(session, message.from_user.id)  # type: ignore
    if not channels:
        await message.answer(_("post.no_channels"))
        return
    await state.set_state(NewPost.choosing_channel)
    await message.answer(
        _("post.choose_channel"), reply_markup=channels_keyboard(channels)
    )


@router.callback_query(NewPost.choosing_channel, F.data.startswith("pch:"))
async def on_channel_chosen(callback: CallbackQuery, state: FSMContext, _):
    if callback.data is None:
        return
    channel_id = int(callback.data.split(":")[1])
    await state.update_data(channel_id=channel_id)
    await state.set_state(NewPost.waiting_content)
    await callback.message.edit_text(_("post.send_content"))  # type: ignore
    await callback.answer()


@router.message(NewPost.waiting_content, F.photo | F.text)
async def on_content(message: Message, state: FSMContext, _):
    if message.photo:
        photo_id = message.photo[-1].file_id
        text = message.caption or ""
    else:
        photo_id = None
        text = message.text
    await state.update_data(text=text, photo_id=photo_id)
    await state.set_state(NewPost.confirming)

    if photo_id:
        await message.answer_photo(photo_id, caption=text)
    else:
        await message.answer(text)  # type: ignore
    await message.answer(_("post.preview"), reply_markup=confirm_keyboard(_))


@router.callback_query(NewPost.confirming, F.data == "post_save")
async def on_save(callback: CallbackQuery, state: FSMContext, session: AsyncSession, _):
    data = await state.get_data()
    await posts_repo.create_draft(
        session, data["channel_id"], data["text"], data["photo_id"]
    )
    await state.clear()
    await callback.message.edit_text(_("post.saved"))  # type: ignore
    await callback.answer()


@router.callback_query(F.data == "post_cancel")
async def on_cancel(callback: CallbackQuery, state: FSMContext, _):
    await state.clear()
    await callback.message.edit_text(_("post.cancelled"))  # type: ignore
    await callback.answer()
