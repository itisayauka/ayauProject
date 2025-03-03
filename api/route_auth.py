from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_session
from app.exceptions import BlogInstanceException
from app.exceptions import UniqueBlogTitleException
from app.models.user import User
from app.service.auth import get_current_user

api_router = APIRouter(prefix="/api", tags=["auth"])

