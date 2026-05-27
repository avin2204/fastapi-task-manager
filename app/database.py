from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)

from dotenv import load_dotenv

import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


# =========================
# SYNCHRONOUS DATABASE
# =========================

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================
# ASYNC DATABASE
# =========================

ASYNC_DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://"
)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


Base = declarative_base()


# =========================
# SYNC DB DEPENDENCY
# =========================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================
# ASYNC DB DEPENDENCY
# =========================

async def get_async_db():

    async with AsyncSessionLocal() as db:

        yield db