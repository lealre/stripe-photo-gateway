from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncSessionLocal
from src.core.redis import pool


async def get_session() -> AsyncGenerator[AsyncSession, None]:  # pragma: no cover
    async with AsyncSessionLocal() as session:
        yield session


async def get_redis() -> AsyncGenerator[Redis, None]:  # pragma: no cover
    redis_client = await Redis(connection_pool=pool)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()


RedisClient = Annotated[Redis, Depends(get_redis)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
