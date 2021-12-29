import pandas as pd

df = pd.read_csv('input.csv', delimiter=';')
# pivot = df.pivot(index='project', columns='month', values='loc')
pivot = df.pivot_table(index='project', columns='month', values='loc', aggfunc = 'sum', fill_value = 'N/A', margins = True, margins_name='Total')
pivot.to_csv('output.csv')