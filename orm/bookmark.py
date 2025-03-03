from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bookmark import Bookmark


async def add_bookmark(db: AsyncSession, user_id: int, dorama_id: int):
    """
    Добавляет дораму в закладки пользователя.
    """
    query = insert(Bookmark).values(user_id=user_id, dorama_id=dorama_id).returning(Bookmark)
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def remove_bookmark(db: AsyncSession, user_id: int, dorama_id: int):
    """
    Удаляет дораму из закладок пользователя.
    """
    query = delete(Bookmark).where(Bookmark.user_id == user_id, Bookmark.dorama_id == dorama_id)
    await db.execute(query)
    await db.commit()


async def get_user_bookmarks(db: AsyncSession, user_id: int):
    """
    Получает список всех закладок пользователя.
    """
    query = select(Bookmark).where(Bookmark.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()
