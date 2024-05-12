from datetime import date, datetime
import os
from typing import AsyncIterator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select
from ..data.entities import Task

# pip install aiosqlite
# pip install pytest-asyncio

# python.py:151: PytestUnhandledCoroutineWarning: async def functions are not natively supported and have been skipped.
#   You need to install a suitable plugin for your async framework, for example:
#     - anyio
#     - pytest-asyncio
#     - pytest-tornasync
#     - pytest-trio
#     - pytest-twisted
#     warnings.warn(PytestUnhandledCoroutineWarning(msg.format(nodeid)))

# pip install anyio
# pip install trio

async def create_async_session_factory(db_file: str) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        'sqlite+aiosqlite:///' + db_file, connect_args={"check_same_thread": False}, echo=False
    )

    factory = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
    return factory


@pytest_asyncio.fixture(name="db", scope="session")
async def with_db_async():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'test_db.sqlite')

    factory = await create_async_session_factory(db_file)
    
    yield factory
    

@pytest.mark.asyncio
async def test_session(db):
    async with db() as session:
        query = select(Task)
        result = await session.scalars(query)
        
        for res in result:
            print(f"{res.id}: {res.name}")
        

@pytest.mark.asyncio
async def test_insert(db):
    async with db() as session:
        task = Task(name="a test task", priority=1, due_date=date.today(), done=False, created_at=datetime.now())
        
        session.add(task)
        await session.commit()
        
        print(task.id)
        assert task.id > 0


@pytest.mark.asyncio
async def test_multiple_actions(db):
    async with db() as session:
        task = Task(name="a test task", priority=1, due_date=date.today(), done=False, created_at=datetime.now())
    
        session.add(task)
        await session.commit()
    
        print(task.id)
        assert task.id > 0

    async with db() as session:
        task = Task(name="a test task", priority=1, due_date=date.today(), done=False, created_at=datetime.now())
        
        session.add(task)
        await session.commit()
        
        print(task.id)
        assert task.id > 0

