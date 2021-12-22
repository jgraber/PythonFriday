import pandas as pd
import numpy as np

df = pd.read_csv('input.csv', delimiter=';')
pivot = df.pivot(index='project', columns='month', values='loc')
pivot.to_csv('output.csv')