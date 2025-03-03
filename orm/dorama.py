from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dorama import Dorama
from app.schemas.dorama import DoramaCreate


async def get_dorama_by_title(db: AsyncSession, title: str):
    """
    Получает дораму по названию.
    """
    query = select(Dorama).filter(Dorama.title == title)
    result = await db.execute(query)
    return result.scalar()


async def create_new_dorama(dorama: DoramaCreate, db: AsyncSession, author_id: int):
    """
    Создает новую дораму.
    """
    query = (
        insert(Dorama)
        .values(
            **dorama.model_dump(),
            author_id=author_id,
            is_active=True
        )
        .returning(Dorama)
    )

    result = await db.execute(query)
    created_dorama = result.scalar()
    await db.commit()
    return created_dorama


async def list_doramas(db: AsyncSession):
    """
    Возвращает список всех дорам.
    """
    query = select(Dorama)
    dorama_list = await db.execute(query)
    return dorama_list.scalars().all()
