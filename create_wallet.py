import asyncio
from uuid import uuid4

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import Wallet
from app.core.config import settings

DATABASE_URL = settings.database_url_local

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def create_wallet():
    async with SessionLocal() as session:
        new_wallet = Wallet(id=uuid4(), balance=0)
        session.add(new_wallet)
        await session.commit()
        print(f"Wallet created with UUID: {new_wallet.id}")


if __name__ == "__main__":
    asyncio.run(create_wallet())
