import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('input.csv', delimiter=';')
df = df.astype({"month": str})
pivot = df.pivot(index='month', columns='project', values='loc')
print(pivot)

ax = pivot.plot()
ax.figure.savefig('test.png')