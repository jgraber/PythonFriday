# no cache

def factorial(n):
    print(f"***{n}***")
    return n * factorial(n-1) if n else 1


factorial(5)
factorial(6)
factorial(8)


# with cache
from functools import cache
@cache
def factorial(n):
    print(f"***{n}***")
    return n * factorial(n-1) if n else 1


factorial(5)
factorial(6)
factorial(8)


"""
>>> from functools import cache
>>> def factorial(n):
...     print(n)
...     return n * factorial(n-1) if n else 1
...
>>>
>>> factorial(5)
5
4
3
2
1
0
120
>>> factorial(6)
6
5
4
3
2
1
0
720
>>> factorial(8)
8
7
6
5
4
3
2
1
0
40320

>>> from functools import cache
>>> @cache
... def factorial(n):
...     print(n)
...     return n * factorial(n-1) if n else 1
...
>>> factorial(5)
5
4
3
2
1
0
120
>>> factorial(6)
6
720
>>> factorial(8)
8
7
40320
"""