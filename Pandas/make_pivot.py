import pandas as pd

df = pd.read_csv('input.csv', delimiter=';')
# create a pivot with just the data:
# pivot = df.pivot(index='project', columns='month', values='loc')
# create a pivot with a total per column and per row:
pivot = df.pivot_table(index='project', columns='month', values='loc', aggfunc = 'sum', fill_value = 'N/A', margins = True, margins_name='Total')
pivot.to_csv('output.csv')