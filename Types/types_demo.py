# from with_types import greeting
from without_types import greeting

a = greeting("Johnny")
a.capitalize


print("*" * 50)


from typing import Callable, Iterator, Union, Optional, Any

# one parameter with a type
def stringify(num: int) -> str:
    return str(num)

result = stringify(1)


# multiple parameters with types
def plus(num1: int, num2: int) -> int:
    return num1 + num2

sum_result = plus(1, 2)

# return type can differ from types of parameters
def division(num1: int, num2: int) -> float:
    return num1 / num2

division_result = division(3, 2)

# lists can have a type
def total(values: list[int]) -> int:
    return sum(values)

print(total([1,2,3,4,5,6,7,8]))

# for dictionaries we can specify the type of the key and of the value
def total_values(input: dict[str, float]) -> float:
    return sum(input.values())

print(total_values({"a": 1.1, "b":3.3}))

# touples with variable size but same type can use ...
def print_tuple(numbers: tuple[int, ...]) -> None:
    for number in numbers:
        print(number)

print_tuple((1,2,3,4))

# booleans can be used as type 
def is_working(a: bool, b: bool) -> bool:
    return a & b

print(is_working(True, True))
print(is_working(True, False))
print(is_working(False, True))
print(is_working(False, False))

print("*" * 50)

def hello(name: Optional[str]) -> None:
    if name:
        print(name)

hello("a")
hello(None)
# hello(1) # works, but type checker will mark it as an error

print("*" * 50)

def printer(values: list[int | str]) -> None:
    for i in values:
        print(i)

printer([1,2,3,4])
printer(["a", "b"])


print("*" * 50)

def whatever(input: Any) -> None:
    pass

print("*" * 50)