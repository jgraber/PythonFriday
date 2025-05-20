import duckdb

duckdb.sql('SELECT extension_name, installed, description FROM duckdb_extensions();').show()


print("*" * 50)


duckdb.sql("INSTALL spatial; LOAD spatial;")
duckdb.sql("SELECT extension_name, installed, description FROM duckdb_extensions() WHERE extension_name = 'spatial'").show()


duckdb.sql("""
    CREATE TABLE points (geom GEOMETRY);

    INSERT INTO points VALUES (ST_Point(1, 2)), (ST_Point(3, 4));

    SELECT ST_Collect(list(geom)) FROM points;
           """).show()

duckdb.sql("SELECT st_distance('POINT(0 0)'::GEOMETRY, 'POINT(1 1)'::GEOMETRY)").show()


print("*" * 50)


duckdb.sql("SELECT * FROM 'https://raw.githubusercontent.com/duckdb/duckdb-web/main/data/weather.csv'").show()

duckdb.sql("SELECT extension_name, installed, description FROM duckdb_extensions() WHERE extension_name = 'httpfs'").show()


print("*" * 50)


duckdb.sql("INSTALL quack FROM community; LOAD quack;")
duckdb.sql("SELECT quack('world');").show()


print("*" * 50)


duckdb.sql("UPDATE EXTENSIONS;")
