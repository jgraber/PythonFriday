# https://numpy.org/doc/stable/reference/routines.set.html
import numpy as np

a = [1,2,3,4]
b = [3,4,5,6]

print(f"a: {a}")
print(f"b: {b}")


in_a_not_in_b = np.setdiff1d(a,b) 
print(f"in a but not in b: {in_a_not_in_b}")

in_b_not_in_a = np.setdiff1d(b,a) 
print(f"in b but not in a: {in_b_not_in_a}")

intersect = np.intersect1d(a,b)
print(f"both in a AND b: {intersect}")

union = np.union1d(a,b)
print(f"everything from a and b: {union}")
