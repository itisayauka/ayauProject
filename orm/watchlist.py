from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate


async def add_to_watchlist(db: AsyncSession, watchlist_data: WatchlistCreate):
    """
    Добавляет дораму в список просмотра пользователя.
    """
    query = insert(Watchlist).values(**watchlist_data.model_dump()).returning(Watchlist)
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def get_user_watchlist(db: AsyncSession, user_id: int):
    """
    Получает список дорам, добавленных пользователем в его список просмотра.
    """
    query = select(Watchlist).where(Watchlist.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def remove_from_watchlist(db: AsyncSession, watchlist_id: int):
    """
    Удаляет дораму из списка просмотра пользователя.
    """
    query = delete(Watchlist).where(Watchlist.id == watchlist_id)
    await db.execute(query)
    await db.commit()
