import pathlib
file_to_rem = pathlib.Path("my_database.db")
file_to_rem.unlink(missing_ok=True)

import duckdb

with duckdb.connect("my_database.db") as con:
    con.sql("CREATE TABLE test (key INTEGER, name VARCHAR)")
    con.sql("INSERT INTO test VALUES (42, 'The answer to life, the universe, and everything')")
    con.table("test").show()

    con.sql("CREATE TABLE people AS FROM 'people.csv'")
    con.table("people").show()


    # con.sql("SELECT Id, count(*) from people group by all order by count(*) desc").show()
    con.sql("CREATE INDEX people_country_idx ON people (Country);")
    con.sql("CREATE UNIQUE INDEX people_id_idx ON people (Id);")

    con.sql("SELECT database_name, schema_name, table_name, estimated_size, column_count FROM duckdb_tables()").show()

    con.sql("DESCRIBE people").show()

    con.sql("DROP TABLE test")