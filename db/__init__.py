from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from settings import SQLALCHEMY_DATABASE_URL, DB_POOL_SIZE, DB_MAX_OVERFLOW

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
)
BaseSQL = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseSQL.metadata.drop_all)
        await conn.run_sync(BaseSQL.metadata.create_all)


async def get_db_session() -> AsyncSession:
    _async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with _async_session() as session:
        yield session
