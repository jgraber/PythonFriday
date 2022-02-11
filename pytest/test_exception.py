def divide(a, b):
    return a / b

# def test_divide():
#     result = divide(10, 0)
    
import pytest

def test_divide_with_0_throws_exception():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)