import duckdb

duckdb.sql("INSTALL excel; LOAD excel;")

duckdb.sql("SELECT * FROM 'demo.xlsx'").show()

duckdb.sql("SELECT * FROM read_xlsx('demo.xlsx', header = true, sheet='Sheet1');").show()


duckdb.sql("CREATE TABLE people AS FROM 'demo.xlsx'")
duckdb.sql("SELECT count(*) AS 'rows' FROM people").show()

data = duckdb.sql("SELECT * FROM 'demo.xlsx' WHERE Age > 30 AND Gender = 'Female'")
data.show()


with duckdb.connect() as con:
    con.install_extension("excel")
    con.load_extension("excel")

    data = con.sql("SELECT * EXCLUDE (Date) FROM 'demo.xlsx' WHERE Age > 20")
    con.sql("COPY data TO 'output.xlsx' WITH (FORMAT xlsx, HEADER true, SHEET 'filtered')")