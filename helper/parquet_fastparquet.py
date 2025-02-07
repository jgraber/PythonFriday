# pip install fastparquet

from fastparquet import write
import pandas as pd

# Sample data
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Write to Parquet file
write('people_fp.parquet', df, compression='GZIP')


print("*" * 75)

from fastparquet import ParquetFile

# Read the Parquet file
pf = ParquetFile('people_fp.parquet')
data = pf.to_pandas().to_dict(orient='list')
print(data)

