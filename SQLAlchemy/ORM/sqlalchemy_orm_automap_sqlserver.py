from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import urllib

Base = automap_base()

SERVER = '.'
DATABASE = 'Northwind'

connection_string = (
    'DRIVER=ODBC Driver 18 for SQL Server;'
    'SERVER=localhost;'
    'DATABASE=Northwind;'
    'Trusted_Connection=yes;'
    'Encrypt=no;'
)
params = urllib.parse.quote_plus(connection_string)
connection_uri = "mssql+pyodbc:///?odbc_connect=%s" % params
engine = create_engine(connection_uri)

# reflect the tables
# Base.prepare(engine, reflect=True, schema='dbo')
Base.prepare(autoload_with=engine, schema='dbo')

# mapped classes use table name.
Customers = Base.classes.Customers

# Show the metadata
# for t in Base.metadata.sorted_tables:
#         print(f"\nTable {t.name}:")
#         for c in t.columns:
#             print(f"{c} ({c.type})")

session = Session(engine)

customers = session.query(Customers).limit(5).all()

for c in customers:
    print(f"{c.CompanyName} - {c.ContactName}: {c.Phone}")

