from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_session
from app.models.user import User
from app.models.review import Review
from app.schemas.review import ReviewCreate, ShowReview, UpdateReview
from app.service.auth import get_current_user
from app.orm import review as review_orm

api_router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@api_router.post("/", response_model=ShowReview, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_schema: ReviewCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await review_orm.create_review(review_schema, db, current_user.id)

@api_router.get("/{review_id}/", response_model=ShowReview)
async def get_review(review_id: int, db: AsyncSession = Depends(get_async_session)):
    return await review_orm.get_review_by_id(review_id, db)

@api_router.get("/", response_model=List[ShowReview])
async def list_reviews(db: AsyncSession = Depends(get_async_session)):
    return await review_orm.get_all_reviews(db)

@api_router.put("/{review_id}/", response_model=ShowReview)
async def update_review(
    review_id: int,
    schema: UpdateReview,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await review_orm.update_review(review_id, schema, db, current_user.id)

@api_router.delete("/{review_id}/")
async def delete_review(
    review_id: int, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)
):
    await review_orm.delete_review(review_id, db, current_user.id)
    return {"status": status.HTTP_200_OK, "detail": "Отзыв удален"}
