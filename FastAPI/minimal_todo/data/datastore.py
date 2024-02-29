from ..models.todo import TaskInput, TaskOutput
from datetime import date

class DataStore:
    def __init__(self):
        self._data = []
        self._id_next = 1
    

    def add(self, entry: TaskInput): 
        extended_entry = TaskOutput(id=self._id_next, 
                                    created_at=date.today(), 
                                    **dict(entry))
        self._data.append(extended_entry)
        self._id_next += 1
        return extended_entry
    

    def all(self):
        return self._data
    

    def get(self, id) -> TaskOutput:
        result = [item for item in self._data if item.id == id]
        if len(result) > 0:
            return result[0]
        else:
            return None
        

    def delete(self, id):
        entry = self.get(id)
        if entry:
            self._data.remove(entry)


    def update(self, id: int, update: TaskInput):
        entry = self.get(id)
        if entry: 
            entry.name = update.name
            entry.priority = update.priority
            entry.due_date = update.due_date
            entry.done = update.done
            return entry
        else: 
            raise ValueError(f"no taks known with id '{id}'")
        
