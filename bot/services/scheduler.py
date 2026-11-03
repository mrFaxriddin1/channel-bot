import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database.models import PostStatus
from bot.repositories import posts as posts_repo

logger = logging.getLogger(__name__)


async def publish_due_posts(bot: Bot, session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        for post in await posts_repo.get_due_posts(session):
            try:
                if post.photo_file_id:
                    await bot.send_photo(
                        post.channel_id, post.photo_file_id, caption=post.text
                    )
                else:
                    await bot.send_message(post.channel_id, post.text)
                await posts_repo.set_status(session, post, PostStatus.SENT)
            except Exception:
                logger.exception("Post %s yuborilmadi", post.id)
                await posts_repo.set_status(session, post, PostStatus.FAILED)


def setup_scheduler(bot: Bot, session_maker: async_sessionmaker) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        publish_due_posts, "interval", seconds=30, args=[bot, session_maker]
    )
    return scheduler
