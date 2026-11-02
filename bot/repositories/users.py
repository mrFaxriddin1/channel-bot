from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_id: int, language: str) -> User:
    user = User(id=user_id, language=language)
    session.add(user)
    await session.commit()
    return user


async def set_language(session: AsyncSession, user_id: int, language: str) -> None:
    user = await session.get(User, user_id)
    if user:
        user.language = language
        await session.commit()
