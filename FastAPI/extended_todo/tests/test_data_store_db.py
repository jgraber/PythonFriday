import os

import pytest_asyncio

from ..models.task_filter import TaskFilter

from ..data.database import create_async_session_factory, create_session_factory
from ..data.datastore_db import DataStoreDb
from ..models.todo import TaskInput
from datetime import date, datetime, timedelta
import pytest


@pytest_asyncio.fixture()
async def with_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'test_db.sqlite')
    
    factory = await create_async_session_factory(db_file)
    yield factory


@pytest.mark.asyncio
async def test_can_add_entry(with_db):
    current_time = datetime.now()
    entry = TaskInput(name="a simple task", 
                      priority=1, 
                      due_date=date.today(), 
                      done=False)
    store = DataStoreDb(with_db)
    
    data = await store.add(entry)

    # since_creation = data.created_at - current_time
    assert data.name == "a simple task"
    assert data.priority == 1
    assert data.due_date == date.today()
    assert data.done == False
    assert data.created_at == date.today()
    # assert since_creation.total_seconds() <= 1
    assert data.id >= 1


@pytest.mark.asyncio
async def test_can_add_multiple_entries(with_db):
    entry_a = TaskInput(name="a simple task", 
                        priority=1, 
                        due_date=date.today(), 
                        done=False)
    entry_b = TaskInput(name="b simple task", 
                        priority=2, 
                        due_date=date.today(), 
                        done=False)
    store = DataStoreDb(with_db)
    
    data_a = await store.add(entry_a)
    data_b = await store.add(entry_b)

    assert data_a.id < data_b.id


@pytest.mark.asyncio
async def test_can_get_specific_entry_back(with_db):
    entry_a = TaskInput(name="Find a specific task", 
                        priority=1, 
                        due_date=date.today(), 
                        done=False)
    store = DataStoreDb(with_db)
    saved = await store.add(entry_a)
    
    entry = await store.get(saved.id)

    # assert entry.id == saved.id
    # assert entry.name == saved.name
    # assert entry.priority == saved.priority
    # assert entry.due_date == saved.due_date
    # assert entry.done == saved.done
    # assert entry.created_at == saved.created_at
    # print(type(entry))
    assert saved == entry


@pytest.mark.asyncio
async def test_missing_entry_gets_None_back(with_db):
    store = DataStoreDb(with_db)

    entry = await store.get(-1)

    assert entry == None


@pytest.mark.asyncio
async def test_can_get_all_entrries_back(with_db):
    entry_a = TaskInput(name="a simple task", 
                        priority=1, 
                        due_date=date.today(), 
                        done=False)
    entry_b = TaskInput(name="b simple task", 
                        priority=2, 
                        due_date=date.today(), 
                        done=False)
    entry_c = TaskInput(name="b simple task", 
                        priority=2, 
                        due_date=date.today(), 
                        done=False)
    store = DataStoreDb(with_db)
    await store.add(entry_a)
    await store.add(entry_b)
    await store.add(entry_c)

    entries = await store.all()
    
    assert len(entries) >= 3


@pytest.mark.asyncio
async def test_can_delete_entry(with_db):
    entry_a = TaskInput(name="a simple task", 
                        priority=1, 
                        due_date=date.today(), 
                        done=False)
    store = DataStoreDb(with_db)
    saved = await store.add(entry_a)
    id = saved.id
    print(id)
    await store.delete(id)
    
    result = await store.get(id)
    assert result == None


@pytest.mark.asyncio
async def test_can_update_entry(with_db):
    old = TaskInput(name="a simple task", 
                    priority=1, 
                    due_date=date.today(), 
                    done=False)
    store = DataStoreDb(with_db)
    old_saved = await store.add(old)

    new = TaskInput(name="b simple task", 
                    priority=2, 
                    due_date=date.today() + timedelta(days=2), 
                    done=True)
    await store.update(old_saved.id, new)

    entry = await store.get(old_saved.id)
    assert entry.name == "b simple task"
    assert entry.priority == 2
    assert entry.due_date == date.today() + timedelta(days=2)
    assert entry.done == True


@pytest.mark.asyncio
async def test_non_existing_entry_cannot_be_updated(with_db):
    store = DataStoreDb(with_db)
    
    new = TaskInput(name="b simple task", 
                    priority=2, 
                    due_date=date.today() + timedelta(days=2), 
                    done=True)
    with pytest.raises(ValueError) as e_info:
        await store.update(-123, new)
    assert str(e_info.value) == "no taks known with id '-123'"


@pytest.mark.asyncio
async def test_fetches_statistics(with_db):
    store = DataStoreDb(with_db)
    await store.add(TaskInput(name="counter", 
                              priority=1, 
                              due_date=date.today(), 
                              done=False))
    stats = await store.get_statistics()

    assert stats.total_tasks == stats.total_open + stats.total_done
    assert stats.total_tasks >= 1


@pytest.mark.asyncio
async def test_filter_empty_filter_gives_all_entries(with_db):
    store = DataStoreDb(with_db)
    await store.add(TaskInput(name="counter", 
                              priority=1, 
                              due_date=date.today(), 
                              done=False))
    await store.add(TaskInput(name="A second entry", 
                              priority=2, 
                              due_date=date.today(), 
                              done=True))
    filter = TaskFilter()
    
    entries = await store.filter(filter)
    
    assert len(entries) >= 2


@pytest.mark.asyncio
async def test_filter_with_filter_for_done_gives_only_done_entries(with_db):
    store = DataStoreDb(with_db)
    await store.add(TaskInput(name="counter", 
                              priority=1, 
                              due_date=date.today(), 
                              done=False))
    await store.add(TaskInput(name="A second entry", 
                              priority=2, 
                              due_date=date.today(), 
                              done=True))
    filter = TaskFilter()
    filter.done = True
    
    entries = await store.filter(filter)
    
    assert len(entries) >= 1

    for entry in entries:
        assert entry.done == True


@pytest.mark.asyncio
async def test_filter_with_filter_for_name_gives_only_matching_entries(with_db):
    store = DataStoreDb(with_db)
    await store.add(TaskInput(name="counter", 
                              priority=1, 
                              due_date=date.today(), 
                              done=False))
    await store.add(TaskInput(name="Create a filter", 
                              priority=2, 
                              due_date=date.today(), 
                              done=True))
    filter = TaskFilter()
    filter.name = "Create a filter"
    
    entries = await store.filter(filter)
    
    assert len(entries) == 1
    assert entries[0].name == "Create a filter"


@pytest.mark.asyncio
async def test_filter_with_search_gives_only_matching_entries(with_db):
    store = DataStoreDb(with_db)
    await store.add(TaskInput(name="Search for item", 
                              priority=1, 
                              due_date=date.today(), 
                              done=False))
    await store.add(TaskInput(name="Create a Search", 
                              priority=2, 
                              due_date=date.today(), 
                              done=True))
    filter = TaskFilter()
    filter.search = "Search"
    
    entries = await store.filter(filter)
    
    assert len(entries) >= 2
    for entry in entries:
        assert "Search" in entry.name
    