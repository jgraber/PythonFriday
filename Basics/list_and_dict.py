data = [1,2,3,4,5]
len(data)


data = [1,2,3,4,5]
more = data.copy()
data.append(6)
data
more


data = [1,2,3,4,5]
data.append(6)
data


data = [1,2,3,4,5]
data.insert(0, 6)
data


data = [1,2,3,4,5]
data.reverse()
data


data = [1,2,3,4,5]
list(reversed(data))
data


data = [1,2,3,4,5]
back = data[::-1]
back
data


data = [1,2,3,4,5]
sum(data)


import numpy as np
data = [1,2,3,4,5]
np.prod(data)

import math
data = [1,2,3,4,5]
math.lcm(*data)

data = [1,2,3,4,5]
min(data)
max(data)


data = [2,4,1,5,3]
data.sort()
data
data.sort(reverse=True)
data


data = [2,4,1,5,3]
sorted(data)
data
sorted(data, reverse=True)
data


from typing import NamedTuple
class Dto(NamedTuple):
    name: str
    value: int

a = Dto("a", 2)
b = Dto("b", 1)
c = Dto("c", 7)
d = Dto("d", 3)
data = [a, d, c, b]
sorted(data, key=lambda x: x.value)
sorted(data, key=lambda x: x.value, reverse=True)
sorted(data, key=lambda x: x.name)
sorted(data, key=lambda x: x.name, reverse=True)


hi = "Hello"
list(hi)


data = ['H', 'e', 'l', 'l', 'o']
"".join(data)

data = ['H', 'e', 'l', 'l', 'o', 1, 2, 3]
"".join(str(x) for x in data)



data = ['H', 'e', 'l', 'l', 'o', 1, 2, 3]
for value in data:
    print(value)


data = ['H', 'e', 'l', 'l', 'o', 1, 2, 3]
for index, value in enumerate(data):
    print(f"{index}. => {value}")


print("*" * 50)

data = {"a":4, "b":2, "d":3, "e":5, "f":1}
max(data.values())

data = {"a":4, "b":2, "d":3, "e":5, "f":1}
max(data.keys())

data = {"a":4, "b":2, "d":3, "e":5, "f":1}
max(data, key=data.get)



"""
>>> data = [1,2,3,4,5]
>>> len(data)
5
>>> data = [1,2,3,4,5]
>>> more = data.copy()
>>> data.append(6)
>>> data
[1, 2, 3, 4, 5, 6]
>>> more
[1, 2, 3, 4, 5]
>>> data = [1,2,3,4,5]
>>> data.append(6)
>>> data
[1, 2, 3, 4, 5, 6]
>>> data = [1,2,3,4,5]
>>> data.insert(0, 6)
>>> data
[6, 1, 2, 3, 4, 5]
>>> data = [1,2,3,4,5]
>>> data.reverse()
>>> data
[5, 4, 3, 2, 1]
>>> data = [1,2,3,4,5]
>>> list(reversed(data))
[5, 4, 3, 2, 1]
>>> data
[1, 2, 3, 4, 5]
>>> data = [1,2,3,4,5]
>>> back = data[::-1]
>>> back
[5, 4, 3, 2, 1]
>>> data
[1, 2, 3, 4, 5]
>>> data = [1,2,3,4,5]
>>> sum(data)
15
>>>
>>> import numpy as np
>>> data = [1,2,3,4,5]
>>> np.prod(data)
120
>>> import math
>>> data = [1,2,3,4,5]
>>> math.lcm(*data)
60
>>> data = [1,2,3,4,5]
>>> min(data)
1
>>> data = [1,2,3,4,5]
>>> max(data)
5
>>> data = [2,4,1,5,3]
>>> data.sort()
>>> data
[1, 2, 3, 4, 5]
>>> data.sort(reverse=True)
>>> data
[5, 4, 3, 2, 1]
>>>
>>> data = [2,4,1,5,3]
>>> sorted(data)
[1, 2, 3, 4, 5]
>>> data
[2, 4, 1, 5, 3]
>>> sorted(data, reverse=True)
[5, 4, 3, 2, 1]
>>> data
[2, 4, 1, 5, 3]
>>> from typing import NamedTuple
>>> class Dto(NamedTuple):
...     name: str
...     value: int
...
>>> a = Dto("a", 2)
>>> b = Dto("b", 1)
>>> c = Dto("c", 7)
>>> d = Dto("d", 3)
>>> data = [a, d, c, b]
>>> sorted(data, key=lambda x: x.value)
[Dto(name='b', value=1), Dto(name='a', value=2), Dto(name='d', value=3), Dto(name='c', value=7)]
>>> sorted(data, key=lambda x: x.value, reverse=True)
[Dto(name='c', value=7), Dto(name='d', value=3), Dto(name='a', value=2), Dto(name='b', value=1)]
>>> sorted(data, key=lambda x: x.name)
[Dto(name='a', value=2), Dto(name='b', value=1), Dto(name='c', value=7), Dto(name='d', value=3)]
>>> sorted(data, key=lambda x: x.name, reverse=True)
[Dto(name='d', value=3), Dto(name='c', value=7), Dto(name='b', value=1), Dto(name='a', value=2)]
>>> hi = "Hello"
>>> list(hi)
['H', 'e', 'l', 'l', 'o']
>>> data = ['H', 'e', 'l', 'l', 'o']
>>> "".join(data)
'Hello'
>>> data = ['H', 'e', 'l', 'l', 'o', 1, 2, 3]
>>> "".join(str(x) for x in data)
'Hello123'
>>> data = ['H', 'e', 'l', 'l', 'o', 1, 2, 3]
>>> for value in data:
...     print(value)
...
H
e
l
l
o
1
2
3
>>> data = ['H', 'e', 'l', 'l', 'o', 1, 2, 3]
>>> for index, value in enumerate(data):
...     print(f"{index}. => {value}")
...
0. => H
1. => e
2. => l
3. => l
4. => o
5. => 1
6. => 2
7. => 3


>>> print("*" * 50)
**************************************************

>>> data = {"a":4, "b":2, "d":3, "e":5, "f":1}
>>> max(data.values())
5
>>>
>>> data = {"a":4, "b":2, "d":3, "e":5, "f":1}
>>> max(data.keys())
'f'
>>>
>>> data = {"a":4, "b":2, "d":3, "e":5, "f":1}
>>> max(data, key=data.get)
'e'
"""