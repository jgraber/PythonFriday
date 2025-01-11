from collections import Counter

input = "a b a c d e f e g e a f d e"
letters = Counter(input)
print(letters)
# Counter({' ': 13, 'e': 4, 'a': 3, 'd': 2, 'f': 2, 'b': 1, 'c': 1, 'g': 1})


input = "abacdefegeafde"
letters = Counter(input)
print(letters)
# Counter({'e': 4, 'a': 3, 'd': 2, 'f': 2, 'b': 1, 'c': 1, 'g': 1})


input = "895266547851256325833554"
numbers = Counter(input)
print(numbers)
# Counter({'5': 7, '8': 3, '2': 3, '6': 3, '3': 3, '4': 2, '9': 1, '7': 1, '1': 1})


input = [8,9,5,2,6,6,5,4,7,8,5,1,2,5,6,3,2,5,8,3,3,5,5,4]
numbers = Counter(input)
print(numbers)
# Counter({5: 7, 8: 3, 2: 3, 6: 3, 3: 3, 4: 2, 9: 1, 7: 1, 1: 1})


input = [89,52,66,5,47,89,125,66,2,5,89,3,3,66,5]
numbers = Counter(input)
print(numbers)
# Counter({89: 3, 66: 3, 5: 3, 3: 2, 52: 1, 47: 1, 125: 1, 2: 1})

fruits = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
fruit_counter = Counter(fruits)
print(fruit_counter)
# Output: Counter({'apple': 3, 'banana': 2, 'orange': 1})

text = "hello world"
char_counter = Counter(text)
print(char_counter)
# Output: Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

print("*" * 50)

initial_counts = {'apple': 2, 'banana': 3}
fruit_counter = Counter(initial_counts)
print(fruit_counter)
# Output: Counter({'banana': 3, 'apple': 2})

fruit_counter = Counter(apple=4, banana=2, orange=1)
print(fruit_counter)
# Output: Counter({'apple': 4, 'banana': 2, 'orange': 1})

print(fruit_counter['apple'])
# Output: 4

print(fruit_counter['grape'])
# Output: 0

fruit_counter.update(['apple', 'banana', 'banana'])
print(fruit_counter)
# Output: Counter({'apple': 5, 'banana': 4, 'orange': 1})

fruit_counter.subtract(['apple', 'orange'])
print(fruit_counter)
# Output: Counter({'apple': 4, 'banana': 4, 'orange': 0})

print(fruit_counter)
# Output: Counter({'apple': 4, 'banana': 4, 'orange': 0})

fruit_counter['apple'] += 1

print(fruit_counter)
# Output: Counter({'apple': 5, 'banana': 4, 'orange': 0})

print(fruit_counter.most_common(2))
# Output: [('apple', 5), ('banana', 4)]


print("*" * 50)

counter1 = Counter(a=3, b=1)
counter2 = Counter(a=1, b=2)

# Addition
print(counter1 + counter2)
# Output: Counter({'a': 4, 'b': 3})

# Subtraction
print(counter1 - counter2)
# Output: Counter({'a': 2})

# Intersection
print(counter1 & counter2)
# Output: Counter({'a': 1, 'b': 1})

# Union
print(counter1 | counter2)
# Output: Counter({'a': 3, 'b': 2})

# Total
print(counter1)
# Counter({'a': 3, 'b': 1})
counter1.total()
# 4