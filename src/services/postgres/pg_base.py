from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine


class PgBase:
    _connection_string: str = "postgresql+asyncpg://leaf:password@localhost:5433/datamart"

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    @asynccontextmanager
    async def _setup_connection(self) -> AsyncGenerator[AsyncSession]:
        try:
            if self._engine is None:
                self._engine = create_async_engine(self._connection_string)

            if self._session_maker is None:
                self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)
                async with self._session_maker() as session:
                    await session.execute(text("SELECT 1"))
            async with self._session_maker() as session:
                yield session
        except OSError as err:
            raise ConnectionError("unable to connect to database") from err
        except Exception as err:
            raise err
