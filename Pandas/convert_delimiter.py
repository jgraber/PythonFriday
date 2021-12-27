import pandas as pd

df = pd.read_csv('input.csv', delimiter=';')
df.to_csv('output_converted.csv', index=False)