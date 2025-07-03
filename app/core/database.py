from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

Base = declarative_base()
engine = create_async_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db():
    async with SessionLocal() as session:
        yield session
