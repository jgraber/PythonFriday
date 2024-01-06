import re
res = re.search("123","123abc123")
type(res)
# <class 're.Match'>
res = re.search("1234","123abc123")
type(res)
# <class 'NoneType'>

res = re.findall("123","123abc123")
res
type(res)
# <class 'list'>
type(res[0])
# <class 'str'>

res = re.finditer("123","123abc123")
for i in res:
    print(i)

# <re.Match object; span=(0, 3), match='123'>
# <re.Match object; span=(6, 9), match='123'>

res = re.findall("\d","123abc123")
res
# ['1', '2', '3', '1', '2', '3']
res = re.findall("\d+","123abc123")
res
# ['123', '123']

res = re.search(r"(\b[A-Z]+\b).+(\b\d+.\d+)","The price of AAPL is 192.34")
res.groups()
# ('APPLE', '192.34')
res.group(1)
# 'APPLE'
res.group(2)
# '192.34'

res = re.search(r"(?P<stock>\b[A-Z]+\b).+(?P<price>\b\d+.\d+)","The price of AAPL is 192.34")
res.groups()
# ('APPLE', '192.34')
res.group("stock")
# 'APPLE'
res.group("price")
# '192.34'


res = re.sub("\d+", "#", "123abc123")
res
# '#abc#'

res, no = re.subn("\d+", "#", "123abc123")
res
# '#abc#'
no
# 2


res = re.sub("123", "#", "123abc123")
res
# '#abc#'

res, no = re.subn("123", "#", "123abc123")
res
# '#abc#'
no
# 2


p = re.compile('[a-z]+')
p.search("abc123cde")
# <re.Match object; span=(0, 3), match='abc'>
p.findall("abc123cde")
# ['abc', 'cde']


regular = "\\w+\\s+\\1"
regular
# '\\w+\\s+\\1'
escaped = r"\w+\s+\1"
escaped
# '\\w+\\s+\\1'


"""
>>> import re
>>> text = "123abc123"
>>> re.search("123",text)
<re.Match object; span=(0, 3), match='123'>
>>> re.search("1234",text)
>>> res = re.search("1234",text)
>>> type(res)
<class 'NoneType'>
>>> res = re.search("1234",text)
>>> type(res)
<class 'NoneType'>
>>> res = re.search("123",text)
>>> type(res)
<class 're.Match'>
>>> res = re.search("1234",text)
>>> type(res)
<class 'NoneType'>
>>> res = re.findall("123",text)
>>> res
['123', '123']
>>> type(res)
<class 'list'>
>>> help(re.findall)
Help on function findall in module re:

findall(pattern, string, flags=0)
    Return a list of all non-overlapping matches in the string.

    If one or more capturing groups are present in the pattern, return
    a list of groups; this will be a list of tuples if the pattern
    has more than one group.

    Empty matches are included in the result.

>>> res = re.findall("1234",text)
>>> type(res)
<class 'list'>
>>> res
[]
>>> res = re.finditer("123",text)
>>> for i in res:
...     print(i)
...
<re.Match object; span=(0, 3), match='123'>
<re.Match object; span=(6, 9), match='123'>
>>> res = re.findall("1234",text)
>>> type(res[0])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
>>> res = re.findall("123",text)
>>> type(res[0])
<class 'str'>
>>> res = re.match("123",text)
>>> res
<re.Match object; span=(0, 3), match='123'>
>>> res = re.match("abc",text)
>>> res
>>> res = re.fullmatch("123",text)
>>> res
>>> res = re.fullmatch("123abc123",text)
>>> res
<re.Match object; span=(0, 9), match='123abc123'>

>>> res = re.findall("\d","123abc123")
>>> res
['1', '2', '3', '1', '2', '3']
>>> res = re.findall("\d+","123abc123")
>>> res
['123', '123']


>>> res = re.search(r"(\b[A-Z]+\b).+(\b\d+.\d+)","The price of APPLE is 192.34")
>>> res.groups()
('APPLE', '192.34')
>>> res.group(1)
'APPLE'
>>> res.group(2)
'192.34'

>>> res = re.search(r"(?P<stock>\b[A-Z]+\b).+(?P<price>\b\d+.\d+)","The price of APPLE is 192.34")
>>> res.groups()
('APPLE', '192.34')
>>> res.group("stock")
'APPLE'
>>> res.group("price")
'192.34'


>>> res = re.sub("\d+", "#", "123abc123")
>>> res
'#abc#'
>>> res, no = re.subn("\d+", "#", "123abc123")
>>> res
'#abc#'
>>> no
2

>>> res = re.sub("123", "#", "123abc123")
>>> res
'#abc#'
>>> res, no = re.subn("123", "#", "123abc123")
>>> res
'#abc#'
>>> no
2

>>> p = re.compile('[a-z]+')
>>> p.search("abc123cde")
<re.Match object; span=(0, 3), match='abc'>
>>> p.findall("abc123cde")
['abc', 'cde']
>>>


>>> regular = "\\w+\\s+\\1"
>>> regular
'\\w+\\s+\\1'
>>> escaped = r"\w+\s+\1"
>>> escaped
'\\w+\\s+\\1'
"""