import os

from ..data.database import create_session_factory
from ..data.datastore_db import DataStoreDb
from ..models.todo import TaskOutput, TaskInput
from datetime import date, datetime, timedelta
import pytest


@pytest.fixture(scope="session")
def with_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'test_db.sqlite')
    
    # if os.path.isfile(db_file):
    #     os.remove(db_file)

    factory = create_session_factory(db_file)
    session = factory()
    
    try:
        yield session
    finally:
        session.close()


def test_can_add_entry(with_db):
    current_time = datetime.now()
    entry = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    store = DataStoreDb(with_db)
    
    data = store.add(entry)

    # since_creation = data.created_at - current_time
    assert data.name == "a simple task"
    assert data.priority == 1
    assert data.due_date == date.today()
    assert data.done == False
    assert data.created_at == date.today()
    # assert since_creation.total_seconds() <= 1
    assert data.id >= 1


def test_can_add_multiple_entries(with_db):
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    entry_b = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    store = DataStoreDb(with_db)
    
    data_a = store.add(entry_a)
    data_b = store.add(entry_b)

    assert data_a.id < data_b.id


def test_can_get_specific_entry_back(with_db):
    entry_a = TaskInput(name="Find a specific task", priority=1, due_date=date.today(), done=False)
    store = DataStoreDb(with_db)
    saved = store.add(entry_a)
    
    entry = store.get(saved.id)

    # assert entry.id == saved.id
    # assert entry.name == saved.name
    # assert entry.priority == saved.priority
    # assert entry.due_date == saved.due_date
    # assert entry.done == saved.done
    # assert entry.created_at == saved.created_at
    # print(type(entry))
    assert saved == entry


def test_missing_entry_gets_None_back(with_db):
    store = DataStoreDb(with_db)

    entry = store.get(-1)

    assert entry == None


def test_can_get_all_entrries_back(with_db):
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    entry_b = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    entry_c = TaskInput(name="b simple task", priority=2, due_date=date.today(), done=False)
    store = DataStoreDb(with_db)
    store.add(entry_a)
    store.add(entry_b)
    store.add(entry_c)

    entries = store.all()
    
    assert len(entries) >= 3


def test_can_delete_entry(with_db):
    entry_a = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    store = DataStoreDb(with_db)
    saved = store.add(entry_a)
    
    store.delete(saved.id)
    
    result = store.get(saved.id)
    assert result == None


def test_can_update_entry(with_db):
    old = TaskInput(name="a simple task", priority=1, due_date=date.today(), done=False)
    store = DataStoreDb(with_db)
    old_saved = store.add(old)

    new = TaskInput(name="b simple task", priority=2, due_date=date.today() + timedelta(days=2), done=True)
    store.update(old_saved.id, new)

    entry = store.get(old_saved.id)
    assert entry.name == "b simple task"
    assert entry.priority == 2
    assert entry.due_date == date.today() + timedelta(days=2)
    assert entry.done == True


def test_non_existing_entry_cannot_be_updated(with_db):
    store = DataStoreDb(with_db)
    
    new = TaskInput(name="b simple task", priority=2, due_date=date.today() + timedelta(days=2), done=True)
    with pytest.raises(ValueError) as e_info:
        store.update(-123, new)
    assert str(e_info.value) == "no taks known with id '-123'"

def test_fetches_statistics(with_db):
    store = DataStoreDb(with_db)
    store.add(TaskInput(name="counter", priority=1, due_date=date.today(), done=False))
    stats = store.get_statistics()

    assert stats.total_tasks == stats.total_open + stats.total_done
    assert stats.total_tasks >= 1