from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_session
from app.models.schedule import Schedule
from app.schemas.schedule import ShowSchedule
from app.orm import schedule as schedule_orm

api_router = APIRouter(prefix="/api/schedule", tags=["schedule"])

@api_router.get("/", response_model=List[ShowSchedule])
async def get_schedule(db: AsyncSession = Depends(get_async_session)):
    return await schedule_orm.get_all_schedules(db)

@api_router.get("/{dorama_id}/", response_model=ShowSchedule)
async def get_schedule_for_dorama(dorama_id: int, db: AsyncSession = Depends(get_async_session)):
    return await schedule_orm.get_schedule_by_dorama_id(dorama_id, db)
