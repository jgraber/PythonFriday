# pip install duckdb
import duckdb

duckdb.sql("SELECT 42").show()

duckdb.sql("SELECT * FROM people.csv").show()

r = duckdb.read_csv("people.csv")
duckdb.sql("SELECT * FROM r").show()

import pandas as pd
df = pd.read_csv('people.csv')
duckdb.sql("SELECT * FROM df").show()

print("#" * 50)

result = duckdb.sql("SELECT Country, count(*) FROM 'people.csv' " \
                    "GROUP BY Country ORDER BY Country")
countries = result.fetchall()
for country in countries:
    print(f"{country[0]} - {country[1]}")


print("#" * 50)

# pandas_df = duckdb.sql("SELECT 42").df()           # Pandas DataFrame
# polars_df = duckdb.sql("SELECT 42").pl()           # Polars DataFrame
# arrow_table = duckdb.sql("SELECT 42").arrow()      # Arrow Table
# numpy_array = duckdb.sql("SELECT 42").fetchnumpy() # NumPy Arrays

print("#" * 50)

duckdb.sql("SELECT 42").write_parquet("out.parquet")
duckdb.sql("SELECT 42").write_csv("out.csv")  
