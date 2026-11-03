from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Channel, Post, User


async def count_users(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(User))
    return result.scalar_one()


async def posts_by_status(session: AsyncSession) -> dict[str, int]:
    result = await session.execute(
        select(Post.status, func.count()).group_by(Post.status)
    )
    return {status.value: count for status, count in result.all()}


async def posts_by_channel(session: AsyncSession) -> list[tuple[str, int]]:
    result = await session.execute(
        select(Channel.title, func.count(Post.id))
        .join(Post, Post.channel_id == Channel.id, isouter=True)
        .group_by(Channel.id, Channel.title)
        .order_by(func.count(Post.id).desc())
    )
    return [(title, count) for title, count in result.all()]
