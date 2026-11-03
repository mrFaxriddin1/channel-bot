from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Channel
from bot.filters.admin import IsAdmin
from bot.repositories import channels as channels_repo

router = Router()


class AddChannel(StatesGroup):
    waiting_forward = State()


@router.message(Command("addchannel"), IsAdmin())
async def cmd_add_channel(message: Message, state: FSMContext, _):
    await state.set_state(AddChannel.waiting_forward)
    await message.answer(_("channel.forward"))


@router.message(AddChannel.waiting_forward, F.forward_origin.type == "channel")
async def on_forward(message: Message, state: FSMContext, session: AsyncSession, _):
    chat = message.forward_origin.chat  # type: ignore
    existing = await session.get(Channel, chat.id)
    if existing:
        await message.answer(_("channel.exists"))
    else:
        await channels_repo.add_channel(
            session, chat.id, chat.title, message.from_user.id  # type: ignore
        )
        await message.answer(_("channel.added", title=chat.title))
    await state.clear()


@router.message(AddChannel.waiting_forward)
async def on_not_forward(message: Message, _):
    await message.answer(_("channel.not_forward"))
