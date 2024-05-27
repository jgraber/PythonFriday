from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from .entitybase import EntityBase


class Task(EntityBase):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name =  Column(String)
    priority = Column(Integer)
    due_date = Column(Date)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime)

    def __str__(self):
        return f"{self.id}: '{self.name}' [{self.due_date}] [{self.done}] - {self.created_at}"
    

class User(SQLAlchemyBaseUserTableUUID, EntityBase):
    pass
