import pytest
from ..models.todo import TaskInput, TaskOutput
from datetime import date, timedelta

def test_create_realistic_input_model():
    input_model = TaskInput(name="write blog post", priority=1, due_date=date.today(), done=False)
    assert input_model.name == "write blog post"
    assert input_model.priority == 1
    assert input_model.due_date == date.today()
    assert input_model.done == False


def test_check_input_has_a_name_larger_than_five():
    with pytest.raises(ValueError) as e_info:
        input_model = TaskInput(name="1234", priority=1, due_date=date.today(), done=False)
    assert "String should have at least 5 characters" in str(e_info.value)


def test_check_input_has_a_name_not_larger_than_100():
    with pytest.raises(ValueError) as e_info:
        input_model = TaskInput(name="x"*101, priority=1, due_date=date.today(), done=False)
    assert "String should have at most 100 characters" in str(e_info.value)
     

def test_check_input_has_a_priority_larger_than_zero():
    with pytest.raises(ValueError) as e_info:
        input_model = TaskInput(name="write blog post", priority=-1, due_date=date.today(), done=False)
    assert "Input should be greater than 0" in str(e_info.value)
    

def test_check_input_has_a_priority_smaler_than_10():
    with pytest.raises(ValueError) as e_info:
        input_model = TaskInput(name="write blog post", priority=10, due_date=date.today(), done=False)
    assert "Input should be less than 10" in str(e_info.value)


def test_check_input_does_not_have_a_due_date_in_the_past():
    with pytest.raises(ValueError) as e_info:
        input_model = TaskInput(name="write blog post", priority=2, due_date=date.today() + timedelta(days=-1), done=False)
    assert f"Input should be greater than or equal to {date.today()}" in str(e_info.value)


def test_check_input_does_not_have_a_due_date_more_than_a_year_in_the_future():
    with pytest.raises(ValueError) as e_info:
            input_model = TaskInput(name="write blog post", priority=2, due_date=date.today() + timedelta(days=+367), done=False)
    assert f"Input should be less than or equal to {date.today() + timedelta(days=+365)}" in str(e_info.value)

