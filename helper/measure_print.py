import timeit

"""
A simplified example on how much print() can cost if you call it in huge numbers.
"""

def with_prints():
    a = 0
    for i in range(0,1000):
        for y in range(0, 1000):
            a += 1
            print(a)
    return a


def without_prints():
    a = 0
    for i in range(0,1000):
        for y in range(0, 1000):
            a += 1
            #print(a)
    return a


if __name__ == '__main__':      
    print(timeit.repeat(with_prints, number=1, repeat=5))
    print(timeit.repeat(without_prints, number=1, repeat=5))
    print(f"number of loops: {without_prints()}")