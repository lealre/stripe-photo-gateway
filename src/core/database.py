from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    expire_on_commit=False,
    autoflush=True,
    bind=engine,
    class_=AsyncSession,
)
