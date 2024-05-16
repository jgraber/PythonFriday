from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import func, text, select
from datetime import date, datetime

from ..models.statistics import StatisticOverview
from ..models.todo import TaskInput, TaskOutput
from .entities import Task

class DataStoreDb:
    def __init__(self, db: AsyncIterator[AsyncSession]):
        self.db = db


    async def add(self, entry: TaskInput) -> TaskOutput:
        async with self.db() as session:
            task = Task(id=None, created_at=datetime.now(), **dict(entry))        
            session.add(task)
            await session.commit()

            return self.__to_output(task) 
        
    
    async def get(self, id: int) -> TaskOutput:
        async with self.db() as session:
            query = select(Task).where(Task.id == id)
            result = await session.scalar(query)
        
        if result:
            return self.__to_output(result)
        else:
            return None
        

    async def all(self):
        async with self.db() as session:
            query = select(Task)
            entries = await session.scalars(query)
        
            results = []

            for entry in entries:
                results.append(self.__to_output(entry))

            return results


    async def delete(self, id: int) -> None:
        async with self.db() as session:
            query = select(Task).where(Task.id == id)
            entry = await session.scalar(query)
                
            if entry:
                await session.delete(entry)
                await session.commit()


    async def update(self, id: int, update: TaskInput) -> TaskOutput:
        async with self.db() as session:
            query = select(Task).where(Task.id == id)
            entry = await session.scalar(query)
            
            if entry: 
                entry.name = update.name
                entry.priority = update.priority
                entry.due_date = update.due_date
                entry.done = update.done
                await session.commit()

                return self.__to_output(entry)
            else: 
                raise ValueError(f"no taks known with id '{id}'")


    async def get_statistics(self) -> StatisticOverview:
        async with self.db() as session:
            query = (
                select(
                    func.count("*").label("total"),
                    func.count("*").filter(Task.done==True).label("done"),
                    func.count("*").filter(Task.done==False).label("open") ,
                )
            )
            result_db = await session.execute(query)
            
            #https://stackoverflow.com/questions/36515882/command-cursor-object-is-not-subscriptable
            result = list(result_db)[0]
            
            return StatisticOverview(total_tasks=result[0], total_done=result[1], total_open=result[2])
    

    def __to_output(self, entity: Task) -> TaskOutput:
        return TaskOutput(id=entity.id, 
                          name=entity.name, 
                          priority=entity.priority, 
                          due_date=entity.due_date,
                          done=entity.done, 
                          created_at=date.today())

