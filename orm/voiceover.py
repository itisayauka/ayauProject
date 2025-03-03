from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.voiceover import Voiceover
from app.schemas.voiceover import VoiceoverCreate


async def add_voiceover(db: AsyncSession, voiceover_data: VoiceoverCreate):
    """
    Добавляет информацию о доступной озвучке для дорамы.
    """
    query = insert(Voiceover).values(**voiceover_data.model_dump()).returning(Voiceover)
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def get_voiceover_by_dorama(db: AsyncSession, dorama_id: int):
    """
    Получает список доступных озвучек для конкретной дорамы.
    """
    query = select(Voiceover).where(Voiceover.dorama_id == dorama_id)
    result = await db.execute(query)
    return result.scalars().all()


async def remove_voiceover(db: AsyncSession, voiceover_id: int):
    """
    Удаляет информацию об озвучке.
    """
    query = delete(Voiceover).where(Voiceover.id == voiceover_id)
    await db.execute(query)
    await db.commit()
