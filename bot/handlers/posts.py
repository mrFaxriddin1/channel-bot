from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.filters.admin import IsAdmin
from bot.keyboards.posts import channels_keyboard, confirm_keyboard, when_keyboard
from bot.repositories import channels as channels_repo
from bot.repositories import posts as posts_repo

router = Router()


class NewPost(StatesGroup):
    choosing_channel = State()
    waiting_content = State()
    confirming = State()
    choosing_when = State()
    waiting_time = State()


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
    post = await posts_repo.create_draft(
        session, data["channel_id"], data["text"], data["photo_id"]
    )
    await state.update_data(post_id=post.id)
    await state.set_state(NewPost.choosing_when)
    await callback.message.edit_text(_("post.when"), reply_markup=when_keyboard(_))  # type: ignore
    await callback.answer()


@router.callback_query(F.data == "post_cancel")
async def on_cancel(callback: CallbackQuery, state: FSMContext, _):
    await state.clear()
    await callback.message.edit_text(_("post.cancelled"))  # type: ignore
    await callback.answer()


@router.callback_query(NewPost.choosing_when, F.data == "when_now")
async def on_now(callback: CallbackQuery, state: FSMContext, session: AsyncSession, _):
    data = await state.get_data()
    await posts_repo.schedule_post(
        session, data["post_id"], datetime.now(timezone.utc)  # noqa: UP017
    )
    await state.clear()
    await callback.message.edit_text(_("post.sent_now"))  # type: ignore
    await callback.answer()


@router.callback_query(NewPost.choosing_when, F.data == "when_later")
async def on_later(callback: CallbackQuery, state: FSMContext, _):
    await state.set_state(NewPost.waiting_time)
    await callback.message.edit_text(_("post.enter_time"))  # type: ignore
    await callback.answer()


@router.message(NewPost.waiting_time, F.text)
async def on_time(message: Message, state: FSMContext, session: AsyncSession, _):
    tz = ZoneInfo(settings.timezone)
    try:
        local = datetime.strptime(message.text.strip(), "%d.%m.%Y %H:%M").replace(  # type: ignore
            tzinfo=tz
        )
    except ValueError:
        await message.answer(_("post.bad_time"))
        return
    when = local.astimezone(timezone.utc)  # noqa: UP017
    if when <= datetime.now(timezone.utc):  # noqa: UP017
        await message.answer(_("post.bad_time"))
        return

    data = await state.get_data()
    await posts_repo.schedule_post(session, data["post_id"], when)
    await state.clear()
    await message.answer(_("post.scheduled", time=local.strftime("%d.%m.%Y %H:%M")))
