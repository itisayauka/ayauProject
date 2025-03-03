from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_session
from app.models.user import User
from app.schemas.user import ShowUser, UpdateUser
from app.service.auth import get_current_user
from app.orm import user as user_orm

api_router = APIRouter(prefix="/api/users", tags=["users"])

@api_router.get("/me/", response_model=ShowUser)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.put("/update/", response_model=ShowUser)
async def update_user(
    user_schema: UpdateUser,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await user_orm.update_user(current_user.id, user_schema, db)

@api_router.delete("/delete/")
async def delete_user(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await user_orm.delete_user(current_user.id, db)
    return {"status": status.HTTP_200_OK, "detail": "Пользователь удален"}
