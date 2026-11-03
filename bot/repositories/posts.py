from datetime import datetime, timezone

from sqlalchemy import select
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


async def schedule_post(session: AsyncSession, post_id: int, when: datetime) -> None:
    post = await session.get(Post, post_id)
    if post:
        post.scheduled_at = when  # type: ignore
        post.status = PostStatus.SCHEDULED
        await session.commit()


async def get_due_posts(session: AsyncSession) -> list[Post]:
    now = datetime.now(timezone.utc)  # noqa: UP017
    result = await session.execute(
        select(Post).where(
            Post.status == PostStatus.SCHEDULED,
            Post.scheduled_at <= now,
        )
    )
    return list(result.scalars().all())


async def set_status(session: AsyncSession, post: Post, status: PostStatus) -> None:
    post.status = status
    await session.commit()
