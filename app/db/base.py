import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session