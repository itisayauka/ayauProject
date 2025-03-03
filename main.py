from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis import asyncio as aioredis

from app.api.route_auth import api_router
from app.config import project_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Настройки подключения брокера
    # https://github.com/long2ice/fastapi-cache#usage
    redis = aioredis.from_url("redis://localhost/")

    print("start app")
    yield
    print("close app")


app = FastAPI(lifespan=lifespan, **project_settings)
app.include_router(auth_route)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
