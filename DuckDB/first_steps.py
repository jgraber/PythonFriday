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





duckdb.sql("SELECT * FROM duckdb_tables()").show()
duckdb.sql("SELECT table_schema, table_name, table_type FROM information_schema.tables;").show()
duckdb.sql("SELECT * FROM 'file_example_CSV_5000.csv' WHERE Country = 'Great Britain'").show()


duckdb.sql("SELECT Country, Gender, count(*) FROM 'people.csv' GROUP BY ALL ORDER BY Country").show()


result = duckdb.sql("SELECT Country, count(*) FROM 'people.csv' GROUP BY Country ORDER BY Country")
countries = result.fetchall()
for country in countries:
    print(f"{country[0]} - {country[1]}")