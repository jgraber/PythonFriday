# https://numpy.org/doc/stable/reference/routines.set.html
import numpy as np

a = [1,2,3,4]
b = [3,4,5,6]

print(type(a))

in_a_not_in_b = np.setdiff1d(a,b) 
print(in_a_not_in_b)

in_b_not_in_a = np.setdiff1d(b,a) 
print(in_b_not_in_a)

intersect = np.intersect1d(a,b)
print(intersect)

union = np.union1d(a,b)
print(union)

unique = np.unique(a,b)
print(unique)