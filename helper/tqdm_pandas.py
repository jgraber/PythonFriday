import pandas as pd
from tqdm import tqdm
import time

tqdm.pandas(desc="Applying function")
df = pd.DataFrame({"A": range(5000)})
df['B'] = df['A'].progress_apply(lambda x: time.sleep(0.001) or x**2)
