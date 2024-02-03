import gc
import time

class Student:
    def __init__(self, name):
        self._name = name


j = Student("Johnny")
print(gc.is_tracked(j))


start = time.perf_counter()
students = []
for i in range(1, 10000000):
    x = Student(str(i))
    students.append(x)
elapsed = time.perf_counter() - start
print(f"GC untouched executed in {elapsed:0.2f} seconds.")

print(gc.get_stats())
print(gc.get_count())
print(gc.get_threshold())
print(len(students))


gc.set_threshold(50000, 100, 100)
start = time.perf_counter()
students = []
for i in range(1, 10000000):
    x = Student(str(i))
    students.append(x)
elapsed = time.perf_counter() - start
print(f"GC modified executed in {elapsed:0.2f} seconds.")

print(gc.get_stats())
print(gc.get_count())
print(gc.get_threshold())
print(len(students))

