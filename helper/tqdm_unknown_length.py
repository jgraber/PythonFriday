from tqdm import tqdm
import time, random

def random_gen():
    while True:
        yield random.random()

for x in tqdm(random_gen(), desc="Working on"):
    time.sleep(0.01)