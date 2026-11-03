from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import IsAdmin
from bot.repositories import stats as stats_repo

router = Router()


@router.message(Command("stats"), IsAdmin())
async def cmd_stats(message: Message, session: AsyncSession, _):
    users = await stats_repo.count_users(session)
    by_status = await stats_repo.posts_by_status(session)
    by_channel = await stats_repo.posts_by_channel(session)

    lines = [_("stats.title"), "", _("stats.users", count=users), ""]

    lines.append(_("stats.posts"))
    if by_status:
        lines += [f"  • {status}: {count}" for status, count in by_status.items()]
    else:
        lines.append(f"  {_('stats.empty')}")

    lines += ["", _("stats.channels")]
    if by_channel:
        lines += [f"  • {title}: {count}" for title, count in by_channel]
    else:
        lines.append(f"  {_('stats.empty')}")

    await message.answer("\n".join(lines))
