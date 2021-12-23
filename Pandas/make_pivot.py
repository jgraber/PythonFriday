import pandas as pd

df = pd.read_csv('input.csv', delimiter=';')
pivot = df.pivot(index='project', columns='month', values='loc')
pivot.to_csv('output.csv')