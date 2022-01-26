import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('input.csv', delimiter=';')
pivot = df.pivot(index='month', columns='project', values='loc')
print(pivot)

ax = pivot.plot()
ax.figure.savefig('test.png')