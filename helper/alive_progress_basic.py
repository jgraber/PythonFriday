from alive_progress import alive_bar
import time

x = 100

with alive_bar(total=x, spinner="circles") as bar:
    for i in range(x):
        time.sleep(.05)
        bar()