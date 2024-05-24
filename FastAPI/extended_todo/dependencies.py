import os

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from .data.entities import User
from .data.database import create_async_session_factory
from .data.datastore_db import DataStoreDb


def db_file():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '.',
        'db',
        'todo_api.sqlite')
    return db_file


async def get_db():
    """
    Creates the datastore 
    """
    
    factory = await create_async_session_factory(db_file())
    db = DataStoreDb(factory)

    yield db
