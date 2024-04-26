from sqlalchemy.orm import Session
from datetime import date, datetime

from ..models.todo import TaskInput, TaskOutput
from .entities import Task

class DataStoreDb:
    def __init__(self, db: Session):
        self.db = db


    def add(self, entry: TaskInput) -> TaskOutput:
        task = Task(created_at=datetime.now(), **dict(entry))        
        self.db.add(task)
        self.db.commit()

        return self.__to_output(task) 
        
    
    def get(self, id: int) -> TaskOutput:
        result = self.db.query(Task) \
            .filter(Task.id == id) \
            .first()
        
        if result:
            return self.__to_output(result)
        else:
            return None
        

    def all(self):
        entries = self.db.query(Task).all()
        results = []

        for entry in entries:
            results.append(self.__to_output(entry))

        return results


    def delete(self, id: int) -> None:
        entry = self.db.query(Task) \
            .filter(Task.id == id) \
            .first()
        
        if entry:
            self.db.delete(entry)
            self.db.commit()


    def update(self, id: int, update: TaskInput) -> TaskOutput:
        entry = self.db.query(Task) \
            .filter(Task.id == id) \
            .first()
        
        if entry: 
            entry.name = update.name
            entry.priority = update.priority
            entry.due_date = update.due_date
            entry.done = update.done
            self.db.commit()

            return self.__to_output(entry)
        else: 
            raise ValueError(f"no taks known with id '{id}'")


    def __to_output(self, entity: Task) -> TaskOutput:
        return TaskOutput(id=entity.id, 
                          name=entity.name, 
                          priority=entity.priority, 
                          due_date=entity.due_date,
                          done=entity.done, 
                          created_at=date.today())

