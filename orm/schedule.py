from sqlalchemy import insert, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


async def add_schedule(db: AsyncSession, schedule_data: ScheduleCreate):
    """
    Добавляет новое расписание выхода серий дорамы.
    """
    query = insert(Schedule).values(**schedule_data.model_dump()).returning(Schedule)
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def update_schedule(db: AsyncSession, schedule_id: int, schedule_data: ScheduleUpdate):
    """
    Обновляет расписание выхода серий.
    """
    query = (
        update(Schedule)
        .where(Schedule.id == schedule_id)
        .values(**schedule_data.model_dump(exclude_unset=True))
        .returning(Schedule)
    )
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def delete_schedule(db: AsyncSession, schedule_id: int):
    """
    Удаляет расписание выхода серий.
    """
    query = delete(Schedule).where(Schedule.id == schedule_id)
    await db.execute(query)
    await db.commit()


async def get_schedule_by_dorama(db: AsyncSession, dorama_id: int):
    """
    Получает расписание выхода серий по ID дорамы.
    """
    query = select(Schedule).where(Schedule.dorama_id == dorama_id)
    result = await db.execute(query)
    return result.scalars().all()
