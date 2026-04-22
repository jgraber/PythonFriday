from alive_progress import alive_bar
import time

x = 100

with alive_bar(total=None, spinner="waves", unknown="flowers", bar="checks") as bar:
    for i in range(x):
        time.sleep(.05)
        bar()