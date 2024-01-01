def append(dic, key, value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]
        


d = {}
append(d, "a", 1)
append(d, "a", 2)
append(d, "b", 1)
print(d)
# {'a': [1, 2], 'b': [1]}
d["a"]
# [1, 2]

from collections import defaultdict
d = defaultdict(list)
d["a"].append(3)
d["a"].append(4)
d["b"].append(5)
print(d)
# defaultdict(<class 'list'>, {'a': [3, 4], 'b': [5]})
d["a"]
# [3, 4]


counters = defaultdict(int)
counters["entry"] += 1
counters["entry"] += 1
counters["exit"] += 1
print(counters)
# defaultdict(<class 'int'>, {'entry': 2, 'exit': 1})


def increment(dic, key, value):
    if key in dic:
        dic[key] += value
    else:
        dic[key] = value

counters = {}
increment(counters, "entry", 1)
increment(counters, "entry", 1)
increment(counters, "exit", 1)
print(counters)
# {'entry': 2, 'exit': 1}