from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

engine = create_engine("mssql+pyodbc://localhost/Northwind?driver=SQL Server?Trusted_Connection=yes")
# reflect the tables
Base.prepare(engine, reflect=True, schema='dbo')

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

