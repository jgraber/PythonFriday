import pandas as pd

d = {'Position': [1, 2, 3], 'Product': ['abcd', '56-8UI.L', 'L1'], 'Size': [90, 1000, 3]}
df = pd.DataFrame(data=d)

print(df)

print("\n\n\n\n")

print(df.to_markdown())

print("\n\n\n\n")

print(df.to_markdown(index=False))

print("\n\n\n\n")

print(df.to_markdown(index=False, tablefmt="latex"))