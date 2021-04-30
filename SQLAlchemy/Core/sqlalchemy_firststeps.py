from sqlalchemy import create_engine
from sqlalchemy import text

connection_string = "sqlite:///Northwind_small.sqlite"
engine = create_engine(connection_string, echo=False)
with engine.begin() as connection:
    result = connection.execute(text("SELECT LastName, FirstName, Title, BirthDate FROM Employee"))
    for row in result:
        print(f"{row['LastName']} {row['FirstName']} ({row['BirthDate']}): \t {row['Title']} ")

