from sqlalchemy import insert, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


async def add_review(db: AsyncSession, user_id: int, dorama_id: int, review_data: ReviewCreate):
    """
    Добавляет новый отзыв к дораме.
    """
    query = insert(Review).values(
        user_id=user_id, dorama_id=dorama_id, **review_data.model_dump()
    ).returning(Review)
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def update_review(db: AsyncSession, review_id: int, review_data: ReviewUpdate, user_id: int):
    """
    Обновляет отзыв пользователя.
    """
    query = (
        update(Review)
        .where(Review.id == review_id, Review.user_id == user_id)
        .values(**review_data.model_dump(exclude_unset=True))
        .returning(Review)
    )
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def delete_review(db: AsyncSession, review_id: int, user_id: int):
    """
    Удаляет отзыв пользователя.
    """
    query = delete(Review).where(Review.id == review_id, Review.user_id == user_id)
    await db.execute(query)
    await db.commit()


async def get_dorama_reviews(db: AsyncSession, dorama_id: int):
    """
    Получает список всех отзывов к дораме.
    """
    query = select(Review).where(Review.dorama_id == dorama_id)
    result = await db.execute(query)
    return result.scalars().all()
