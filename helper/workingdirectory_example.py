import os

current = os.getcwd()
print(current)
#-> D:\Python\PythonFriday\helper

os.chdir('C:\Temp')

new_dir = os.getcwd()
print(new_dir)
#-> C:\Temp