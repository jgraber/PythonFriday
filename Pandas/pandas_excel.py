import pandas as pd

df = pd.read_excel('../DuckDB/demo.xlsx', index_col=0, dtype_backend='pyarrow')

print(df.info())

print("\n\n\n")

print(df)


print("\n\n\n")

data = df[df.Country == 'Great Britain']
print(data)

print("\n\n\n")

data.to_excel('output.xlsx', index=True, sheet_name='GB')