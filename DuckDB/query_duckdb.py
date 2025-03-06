# pip install duckdb
import duckdb


r = duckdb.read_csv("people.csv")
duckdb.sql("SELECT * FROM r").show()

duckdb.sql('SELECT "First Name", "Last Name", Age FROM r').show()


print("*" * 50)


duckdb.sql("SELECT * EXCLUDE (Country) FROM r").show()

duckdb.sql("SELECT * EXCLUDE (Country, Age) FROM r").show()

duckdb.sql("SELECT * REPLACE (lower(Country) AS Country) FROM r").show()

duckdb.sql("SELECT t.i FROM range(10, 25) AS t(i)").show()


print("*" * 50)


duckdb.sql("SELECT * FROM range(10, 25) AS t(i) JOIN r on r.Age == t.i").show()


print("*" * 50)


duckdb.sql("SELECT Country, Age, count(*) FROM r GROUP BY ALL").show()


print("*" * 50)


duckdb.sql("SELECT * FROM r ORDER BY Id LIMIT 5 OFFSET 20").show()


print("*" * 50)


duckdb.sql("SELECT * FROM r TABLESAMPLE 5 ROWS").show()

duckdb.sql("SELECT * FROM r TABLESAMPLE 10%;").show()


duckdb.sql("SELECT * FROM r USING SAMPLE  5 ROWS;").show()

duckdb.sql("SELECT * FROM r USING SAMPLE 1% (bernoulli);").show()

duckdb.sql("SELECT t.i FROM range(1000) AS t(i) USING SAMPLE 5 ROWS;").show()

duckdb.sql("SELECT t.i FROM range(1000) AS t(i) USING SAMPLE 1% (bernoulli);").show()


print("*" * 50)


duckdb.sql("SELECT min(COLUMNS(*)) FROM r").show()

