from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String

from .entitybase import EntityBase


class Task(EntityBase):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name =  Column(String)
    priority = Column(Integer)
    due_date = Column(Date)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime)
