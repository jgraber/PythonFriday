import pandas as pd

# df = pd.read_csv('input.csv', delimiter=';')
# # create a pivot with just the data:
# # pivot = df.pivot(index='project', columns='month', values='loc')
# # create a pivot with a total per column and per row:
# pivot = df.pivot_table(index='project', columns='month', values='loc', aggfunc = 'sum', fill_value = 'N/A', margins = True, margins_name='Total')
# pivot.to_csv('output.csv')
# load the data into a data frame
df = pd.read_csv('input.csv', delimiter=';')

# create a pivot with just the data:
pivot = df.pivot(index='project', columns='month', values='loc')
print(pivot)

# export pivot to CSV
pivot.to_csv('output.csv')


print("\n-------\n")

# create a pivot with a grand total column & row
pt = df.pivot_table(index='project', columns='month', values='loc', 
                    aggfunc = 'sum', fill_value = 'N/A', 
                    margins = True, margins_name='Total')
print(pt)

# export pivot table to CSV
pt.to_csv('output_table.csv')