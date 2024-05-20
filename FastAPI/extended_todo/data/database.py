from typing import AsyncIterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def create_session_factory(db_file: str) -> sessionmaker:
    engine = create_engine(
        'sqlite:///' + db_file, connect_args={"check_same_thread": False}, echo=False
    )

    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return factory


async def create_async_session_factory(db_file: str) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        'sqlite+aiosqlite:///' + db_file, connect_args={"check_same_thread": False}, echo=False
    )

    factory = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)
    return factory