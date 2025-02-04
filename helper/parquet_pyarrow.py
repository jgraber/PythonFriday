# pip install pyarrow

import pyarrow as pa
import pyarrow.parquet as pq

# Sample data
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}

# Create a Table
table = pa.table(data)

# Write to Parquet file
pq.write_table(table, 'people.parquet')


print("*" * 75)


# Read the Parquet file
table = pq.read_table('people.parquet')

# Convert to a dictionary
data = table.to_pydict()
print(data)
