import time
from tqdm import tqdm

for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.05)