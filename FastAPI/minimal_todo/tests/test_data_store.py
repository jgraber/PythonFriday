from ..data.datastore import DataStore
from ..models.todo import TaskOutput, TaskInput
from datetime import date, timedelta
import pytest

def test_created_store_is_empty():
    store = DataStore()
    
    data = store.all()

    assert data == []

def test_can_add_entry():
    entry = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    store = DataStore()
    
    data = store.add(entry)

    assert data.name == "a simple task"
    assert data.priority == 1
    assert data.due_date == date.today()
    assert data.done == False
    assert data.created_at == date.today()
    assert data.id == 1


def test_can_add_multiple_entries():
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    entry_b = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    store = DataStore()
    
    data_a = store.add(entry_a)
    data_b = store.add(entry_b)

    assert data_a.id < data_b.id


def test_can_get_specific_entry_back():
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    entry_b = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    store = DataStore()
    store.add(entry_a)
    store.add(entry_b)

    entry = store.get(2)

    assert entry.name == "b simple task"


def test_missing_entry_gets_None_back():
    store = DataStore()

    entry = store.get(2)

    assert entry == None


def test_can_get_all_entrries_back():
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    entry_b = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    entry_c = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    store = DataStore()
    store.add(entry_a)
    store.add(entry_b)
    store.add(entry_c)

    entries = store.all()
    
    assert len(entries) == 3

def test_can_delete_entry():
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    entry_b = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    store = DataStore()
    store.add(entry_a)
    store.add(entry_b)
    
    store.delete(2)
    
    entries = store.all()
    assert len(entries) == 1
    assert entries[0].id == 1

def test_can_update_entry():
    old = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    store = DataStore()
    store.add(old)

    new = TaskInput(name="b simple task", priority=2, due_date=date.today() + timedelta(days=2), done=True)
    store.update(1, new)

    entry = store.get(1)
    assert entry.name == "b simple task"
    assert entry.priority == 2
    assert entry.due_date == date.today() + timedelta(days=2)
    assert entry.done == True

def test_non_existing_entry_cannot_be_updated():
    store = DataStore()
    
    new = TaskInput(name="b simple task", priority=2, due_date=date.today() + timedelta(days=2), done=True)
    with pytest.raises(ValueError) as e_info:
        store.update(123, new)
    assert str(e_info.value) == "no taks known with id '123'"