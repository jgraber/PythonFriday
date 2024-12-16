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