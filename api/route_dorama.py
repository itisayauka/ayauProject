from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_session
from app.models.user import User
from app.models.dorama import Dorama
from app.schemas.dorama import DoramaCreate, ShowDorama, UpdateDorama
from app.service.auth import get_current_user
from app.orm import dorama as dorama_orm

api_router = APIRouter(prefix="/api/doramas", tags=["doramas"])

@api_router.post("/", response_model=ShowDorama, status_code=status.HTTP_201_CREATED)
async def create_dorama(
    dorama_schema: DoramaCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await dorama_orm.create_dorama(dorama_schema, db, current_user.id)

@api_router.get("/{dorama_id}/", response_model=ShowDorama)
async def get_dorama(dorama_id: int, db: AsyncSession = Depends(get_async_session)):
    return await dorama_orm.get_dorama_by_id(dorama_id, db)

@api_router.get("/", response_model=List[ShowDorama])
async def list_doramas(db: AsyncSession = Depends(get_async_session)):
    return await dorama_orm.get_all_doramas(db)

@api_router.put("/{dorama_id}/", response_model=ShowDorama)
async def update_dorama(
    dorama_id: int,
    schema: UpdateDorama,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await dorama_orm.update_dorama(dorama_id, schema, db, current_user.id)

@api_router.delete("/{dorama_id}/")
async def delete_dorama(
    dorama_id: int, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)
):
    await dorama_orm.delete_dorama(dorama_id, db, current_user.id)
    return {"status": status.HTTP_200_OK, "detail": "Дорама удалена"}
