import pandas as pd

# Sample DataFrame
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}
df = pd.DataFrame(data)

# Write to Parquet file
df.to_parquet('people.parquet')


print("*" * 75)


# Read the Parquet file
df = pd.read_parquet('people.parquet')

# Display the DataFrame
print(df)


print("*" * 75)


df = pd.read_parquet('people.parquet', columns=['name', 'age'])
print(df)