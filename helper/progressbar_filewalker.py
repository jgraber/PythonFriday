import time
import progressbar
import os

def do_something(file):
	print(file)
	time.sleep(0.02)

files = os.listdir('D:\Python')

for i in progressbar.progressbar(files):
	do_something(i)
    