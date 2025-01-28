import redis.asyncio as redis

from src.core.settings import settings


def create_redis_pool() -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


pool = create_redis_pool()
