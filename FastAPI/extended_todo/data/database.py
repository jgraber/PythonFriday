from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .__all_models import *
from .entitybase import EntityBase

def create_session_factory(db_file: str) -> sessionmaker:
    engine = create_engine(
        'sqlite:///' + db_file, connect_args={"check_same_thread": False}
    )

    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return factory
