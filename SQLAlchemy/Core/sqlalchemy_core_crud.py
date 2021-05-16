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

def select_all():
    stmt = select(employees)
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        rs = con.execute(stmt)
        for row in rs:
            print(row)


def select_partial():
    stmt = select(employees.c.LastName, employees.c.FirstName).where(employees.c.Id == 30)
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        rs = con.execute(stmt)
        for row in rs:
            print(row)
        
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


def select_by_first_and_last_name():
    stmt = select(employees).\
        where((employees.c.LastName == "Leverling") & (employees.c.FirstName == "Janet"))
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result)            

def select_multiple_where():
    stmt = select(employees).\
        where(employees.c.LastName == "Leverling").\
        where(employees.c.FirstName == "Janet")
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result) 


def select_by_first_or_last_name():
    stmt = select(employees).\
        where((employees.c.LastName == "Leverling") | (employees.c.FirstName == "Andrew"))
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result)    


def select_or_():
    stmt = select(employees).\
        where(
            or_(
                employees.c.LastName == "Leverling", employees.c.FirstName == "Andrew")
            )
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result)    


def select_contains():
    stmt = select(employees).\
        where(
            employees.c.LastName.contains("u")
            )
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result) 

def select_startswith():
    stmt = select(employees).\
        where(
            employees.c.LastName.startswith("D")
            )
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result) 
            
            
def select_endswith():
    stmt = select(employees).\
        where(
            employees.c.LastName.endswith("n")
            )
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=True)
    with engine.begin() as con:
        results = con.execute(stmt).all()
        for result in results:
            print(result) 
            

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
    print("---- select_by_first_and_last_name() ----")  
    select_by_first_and_last_name()
    print("---- select_multiple_where() ----")
    select_multiple_where()
    print("---- select_by_first_or_last_name() ----")
    select_by_first_or_last_name()
    print("---- select_or_() ----")
    select_or_()
    print("---- select_contains() ----")
    select_contains()
    print("---- select_startswith() ----")
    select_startswith()
    print("---- select_endswith() ----")
    select_endswith()
    # print("---- select_all() ----")
    # select_all()
    # print("---- select_by_id() ----")   
    # select_by_id()
    # print("---- select_partial() ----")
    # select_partial()
    # statement_infos()
    # print("---- end ----")
           
# https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-core/    