import os

from .data.database import create_async_session_factory, create_session_factory
from .data.datastore_db import DataStoreDb


async def get_db():
    """
    Creates the datastore 
    """
    db_file = os.path.join(
        os.path.dirname(__file__),
        '.',
        'db',
        'todo_api.sqlite')
    
    factory = await create_async_session_factory(db_file)
    db = DataStoreDb(factory)

    yield db
    