from sqlalchemy import MetaData, Table, Column, String, Integer, Text, DateTime, Boolean, create_engine, select, insert, update, delete, or_

metadata = MetaData()

employees = Table('Employee', metadata,
                 Column('Id', Integer(), primary_key=True),
                 Column('LastName', String(8000)),
                 Column('FirstName', String(8000)),
                 Column('BirthDate', String(8000))
)

def show_metadata():
    for t in metadata.sorted_tables:
        print(f"Table {t.name}:")
        for c in t.columns:
            print(f"{c} ({c.type})")

        
def do_insert():
    stmt = insert(employees).values(
        LastName='Collins', 
        FirstName='Arnold', 
        BirthDate='2000-01-31')
    new_id = 0
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        result = con.execute(stmt)
        new_id = result.inserted_primary_key['Id']
        print(f"New Id: {new_id}")
        
    return new_id


def select_by_id(id):
    stmt = select(employees).where(employees.c.Id == id)
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        result = con.execute(stmt).first()
        if result:
            print(result)            
        else:
            print(f"no rows found with Id == {id}")
   

def do_update(id):
    stmt = update(employees).values(
        FirstName="Michael"
        ).where(employees.c.Id == id)
        
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(stmt)

        
def do_delete(id):
    stmt = delete(employees).where(employees.c.Id == id)
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(stmt)

        
def statement_infos():
    stmt = select(employees.c.LastName, employees.c.FirstName).where(employees.c.Id == 30)
    print(f"statement with placeholder: \n{str(stmt)}")
    print(f"\nparams: \n{str(stmt.compile().params)}")

        
if __name__ == '__main__':
    print("---- show_metadata() ----")
    show_metadata()
    print("---- do_insert() ----")
    id = do_insert()
    print("---- select_by_id() ----")   
    select_by_id(id)
    print("---- do_update() ----")
    do_update(id)
    select_by_id(id)
    print("---- do_delete() ----")   
    do_delete(id) 
    select_by_id(id)
    print("---- end ----")
           
# https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-core/    