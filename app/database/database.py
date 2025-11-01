from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app.core.config import settings


class Database:
    def __init__(
        self,
        db_url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 1800,
    ):
        self._engine: AsyncEngine = create_async_engine(
            db_url,
            echo=echo,
            future=True,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )

        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def check_connection(self) -> bool:
        try:
            async with self._engine.connect() as conn:
                result = await conn.execute(sa.text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            return False

    @property
    def session_factory(self) -> Callable[[], AsyncSession]:
        return self._session_factory

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    async def dispose(self) -> None:
        await self._engine.dispose()


_db_instance: Database | None = None


def get_database() -> Database:
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(settings.database_url)
    return _db_instance


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db = get_database()
    async with db.session() as session:
        yield session
