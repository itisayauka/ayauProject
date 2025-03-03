from datetime import datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import jwt_token_settings
from app.database import get_async_session
from app.models.user import User
from app.orm.user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token/")


async def create_access_token(user: User):
    """
    Функция создания JWT токена для пользователя.
    """
    token_exp_time = int(datetime.now().timestamp()) + jwt_token_settings.TOKEN_LIFESPAN

    payload = {"username": user.username, "email": user.email, "exp": token_exp_time}

    token = jwt.encode(
        payload,
        jwt_token_settings.JWT_SECRET_KEY,
        algorithm=jwt_token_settings.VERIFY_SIGNATURE,
    )
    return token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
):
    """
    Функция получения текущего пользователя по JWT токену.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            jwt_token_settings.JWT_SECRET_KEY,
            algorithms=[jwt_token_settings.VERIFY_SIGNATURE],
        )
        username = payload.get("username")

        if username is None:
            raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature has expired",
        )

    except DecodeError:
        raise credentials_exception

    user = await get_user_by_username(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user
