from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Channel


async def add_channel(
    session: AsyncSession, channel_id: int, title: str, owner_id: int
) -> Channel:
    channel = Channel(id=channel_id, title=title, owner_id=owner_id)
    session.add(channel)
    await session.commit()
    return channel


async def get_channels(session: AsyncSession, owner_id: int) -> list[Channel]:
    result = await session.execute(select(Channel).where(Channel.owner_id == owner_id))
    return list(result.scalars().all())
