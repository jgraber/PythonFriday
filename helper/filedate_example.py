import filedate
from pathlib import Path

a = 'test_data/aa.txt'
Path(a).write_text("")

a_file = filedate.File(a)
print(a_file.get())

a_file = filedate.File(a)
a_file.set(
    created = "2022.01.01 13:00:00",
    modified = "2022.01.01 14:00:00",
    accessed = "2022.01.01 15:00:00"
)

after = filedate.File(a)
print(after.get())