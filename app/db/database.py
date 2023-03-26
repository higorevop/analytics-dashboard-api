import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


Base = declarative_base()

load_dotenv()

DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://dev_username:dev_password@localhost/analytics")

engine = create_async_engine(DATABASE_URL)

database = Database(DATABASE_URL)

async def get_db() -> AsyncGenerator:
    async with database.transaction():
        yield database

async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)