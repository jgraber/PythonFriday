import random
from datetime import datetime

def random_int():
    """
    Returns an integer between 0 and 10
    
    >>> random.seed(111)
    >>> random_int()   
    3
    >>> random_int()
    5
    >>> random_int()
    7
    
    """
    return random.randint(0, 10)

def dynamic_text():
    """
    Returns the current time:
    
    >>> dynamic_text() # doctest: +SKIP
    'It is now 14:52:45'
    
    >>> dynamic_text() # doctest: +ELLIPSIS 
    'It is now ...'
    
    """
    now = datetime.now().strftime("%H:%M:%S")
    return f"It is now {now}"

def exception_demo():
    """
    >>> exception_demo()
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "D:\Python\dynamicoutputNOOOO.py", line 0, in exception_demo
            1 / 0
    ZeroDivisionError: division by zero

    """
    1 / 0