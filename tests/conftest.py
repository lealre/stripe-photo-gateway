from collections.abc import AsyncGenerator, Generator
from typing import Literal

import boto3
import pytest
from httpx import ASGITransport, AsyncClient
from moto import mock_aws
from botocore import client
from redis.asyncio import Redis as asyncRedis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import AsyncRedisContainer

from src.api.dependencies import get_redis, get_session
from src.app import app
from src.models import Base

BASE_URL = 'http://test'


@pytest.fixture(autouse=True, scope='session')
def anyio_backend() -> Literal['asyncio']:
    return 'asyncio'


@pytest.fixture(scope='session')
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer('postgres:16', driver='asyncpg') as postgres:
        yield postgres


@pytest.fixture(scope='session')
def redis_container() -> Generator[AsyncRedisContainer, None]:
    with AsyncRedisContainer() as container:
        yield container


@pytest.fixture
async def redis_client(
    redis_container: AsyncRedisContainer,
) -> AsyncGenerator[asyncRedis, None]:
    redis_client: asyncRedis = await redis_container.get_async_client()
    await redis_client.flushdb()
    yield redis_client
    await redis_client.close()


@pytest.fixture
async def async_session(
    postgres_container: PostgresContainer,
) -> AsyncGenerator[AsyncSession, None]:
    async_db_url = postgres_container.get_connection_url()
    async_engine = create_async_engine(async_db_url, pool_pre_ping=True)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with async_session() as as_session:
        yield as_session


@pytest.fixture
async def async_client(
    async_session: AsyncSession, redis_client: asyncRedis
) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: redis_client

    _transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=_transport, base_url=BASE_URL, follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def s3_client() -> Generator[client.BaseClient, None, None]:
    with mock_aws():
        s3_client = boto3.client('s3')
        yield s3_client
