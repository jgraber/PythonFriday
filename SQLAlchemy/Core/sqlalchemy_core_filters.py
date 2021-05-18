from sqlalchemy import MetaData, Table, Column, String, Integer, Text, DateTime, Boolean, create_engine, select, insert, update, delete, or_, and_

metadata = MetaData()

employees = Table('Employee', metadata,
                 Column('Id', Integer(), primary_key=True),
                 Column('LastName', String(8000)),
                 Column('FirstName', String(8000)),
                 Column('BirthDate', String(8000))
)

def print_result(stmt):
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        rs = con.execute(stmt)
        for row in rs:
            print(row) 


def select_all():
    stmt = select(employees)
    
    print_result(stmt)


def select_equals():
    stmt = select(employees).\
        where(employees.c.Id == 1)
    
    print_result(stmt)
    
def select_not_equals():
    stmt = select(employees).\
        where(employees.c.Id != 1)
    
    print_result(stmt)
    

def select_greather_than():
    stmt = select(employees).\
        where(employees.c.Id > 5)
    
    print_result(stmt)


def select_less_than():
    stmt = select(employees).\
        where(employees.c.Id < 3)
    
    print_result(stmt)
        

def select_like():
    stmt = select(employees).\
        where(
            employees.c.LastName.like("Pe%k")
            )
        
    print_result(stmt)


def select_not_like():
    stmt = select(employees).\
        where(
            employees.c.LastName.not_like("Pe%k")
            )
    
    print_result(stmt)

    
def select_contains():
    stmt = select(employees).\
        where(
            employees.c.LastName.contains("u")
            )
    
    print_result(stmt)


def select_startswith():
    stmt = select(employees).\
        where(
            employees.c.LastName.startswith("D")
            )
    
    print_result(stmt)
            
            
def select_endswith():
    stmt = select(employees).\
        where(
            employees.c.LastName.endswith("n")
            )
    
    print_result(stmt)    
    
    
def select_in_():
    stmt = select(employees).\
        where(employees.c.Id.in_([1,2,3]))
    
    print_result(stmt)
    
    
def select_not_in():
    stmt = select(employees).\
        where(employees.c.Id.not_in([1,2,3]))
    
    print_result(stmt)    
    
    
        
def select_with_python_and():
    stmt = select(employees).\
        where(
            (employees.c.LastName == "Leverling") & (employees.c.FirstName == "Janet")
            )

    print_result(stmt)           


def select_and_():
    stmt = select(employees).\
        where(
            and_(
                (employees.c.LastName == "Leverling"), (employees.c.FirstName == "Janet")
                )
            )
    
    print_result(stmt) 


def select_multiple_where():
    stmt = select(employees).\
        where(employees.c.LastName == "Leverling").\
        where(employees.c.FirstName == "Janet")
    
    print_result(stmt)


def select_with_pyton_or():
    stmt = select(employees).\
        where((employees.c.LastName == "Leverling") | (employees.c.FirstName == "Andrew"))
    
    print_result(stmt) 


def select_or_():
    stmt = select(employees).\
        where(
            or_(
                employees.c.LastName == "Leverling", employees.c.FirstName == "Andrew"
                )
            )
    
    print_result(stmt)   





def select_partial():
    stmt = select(employees.c.LastName, employees.c.FirstName).where(employees.c.Id == 4)
    
    print_result(stmt)
            

if __name__ == '__main__':
    print("---- select_all() ----")  
    select_all()
    
    print("---- select_equals() ----")  
    select_equals()    
    print("---- select_not_equals() ----")  
    select_not_equals()
    
    print("---- select_greather_than() ----")  
    select_greather_than()
    print("---- select_less_than() ----")  
    select_less_than()
    
    print("---- select_like() ----")  
    select_like()
    print("---- select_not_like() ----")  
    select_not_like()
    print("---- select_contains() ----")
    select_contains()
    print("---- select_startswith() ----")
    select_startswith()
    print("---- select_endswith() ----")
    select_endswith()
    
    print("---- select_in_() ----")
    select_in_()
    print("---- select_not_in() ----")
    select_not_in()
    
    
    print("---- select_with_python_and() ----")  
    select_with_python_and()
    print("---- select_and_() ----")    
    select_and_()
    print("---- select_multiple_where() ----")
    select_multiple_where()
    
    print("---- select_with_pyton_or() ----")
    select_with_pyton_or()
    print("---- select_or_() ----")
    select_or_()
    
    print("---- select_partial() ----")
    select_partial()
    print("---- end ----")
           
# https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-core/    