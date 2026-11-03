from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Post, PostStatus


async def create_draft(
    session: AsyncSession, channel_id: int, text: str, photo_file_id: str | None
) -> Post:
    post = Post(
        channel_id=channel_id,
        text=text,
        photo_file_id=photo_file_id,
        status=PostStatus.DRAFT,
    )
    session.add(post)
    await session.commit()
    return post
