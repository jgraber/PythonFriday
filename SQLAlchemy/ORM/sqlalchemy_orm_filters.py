"""
Example on how to use filters in the ORM part of SQLAlchemy
"""
import os
from datetime import datetime
import data.db_session as db_session
from data.employee import Employee
from sqlalchemy import or_, and_
    
def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'Northwind_small.sqlite')
    db_session.global_init(db_file)


def print_result(result):
    for entry in result:
        print(entry)


def query_all():
    session = db_session.factory()
    
    for employe in session.query(Employee):
        print(employe)
        
    session.close()  


def query_equals():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id == 1):
        print(employe)
        
    session.close()  
    
    
def query_not_equals():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id != 1):
        print(employe)
        
    session.close() 


def query_greather_than():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id > 5):
        print(employe)
        
    session.close() 


def query_less_than():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id < 3):
        print(employe)
        
    session.close() 


def query_like():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.last_name.like("Pe%k")):
        print(employe)
        
    session.close() 
    
    
def query_not_like():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.last_name.not_like("Pe%k")):
        print(employe)
        
    session.close() 
    
    
def query_contains():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.last_name.contains("u")):
        print(employe)
        
    session.close() 
    

def query_startswith():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.last_name.startswith("D")):
        print(employe)
        
    session.close() 
    
    
def query_endswith():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.last_name.endswith("n")):
        print(employe)
        
    session.close()   


def query_in_():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id.in_([1,2,3])):
        print(employe)
        
    session.close()
    
    
def query_in_negated():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(~Employee.id.in_([1,2,3])):
        print(employe)
        
    session.close()
    
        
def query_not_in():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id.not_in([1,2,3])):
        print(employe)
        
    session.close()    


def query_multiple_filter_in_one():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id == 7, Employee.last_name == "King"):
        print(employe)
        
    session.close()  


def query_and_():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(and_(Employee.id == 7, Employee.last_name == "King")):
        print(employe)
        
    session.close()  


def query_multiple_filter():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id == 7).\
        filter(Employee.last_name == "King"):
        print(employe)
        
    session.close()  


def query_or_():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(or_(Employee.id == 2, Employee.id == 3)):
        print(employe)
        
    session.close()  

# Works in Core, not in ORM
def query_with_python_or_():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id == 2 | Employee.id == 3):
        print(employe)
        
    session.close()  

def query_with_python_and_fails():
    session = db_session.factory()
    
    for employe in session.query(Employee).\
        filter(Employee.id == 7 & Employee.last_name == "King"):
        print(employe)
        # throws exception
        
    session.close()  
    

if __name__ == '__main__':
    print("--- setup_db() ---")
    setup_db()
    print("--- query_all() ---")
    query_all()
    print("--- query_equals() ---")
    query_equals()
    print("--- query_not_equals() ---")
    query_not_equals()
    print("--- query_greather_than() ---")
    query_greather_than()
    print("--- query_less_than() ---")
    query_less_than()
    print("--- query_like() ---")
    query_like()
    print("--- query_not_like() ---")
    query_not_like()
    print("--- query_contains() ---")
    query_contains()
    print("--- query_startswith() ---")
    query_startswith()
    print("--- query_endswith() ---")
    query_endswith()
    print("--- query_in_() ---")
    query_in_()
    print("--- query_in_negated() ---")
    query_in_negated()
    print("--- query_not_in() ---")
    query_not_in()    
    print("--- query_multiple_filter_in_one() ---")
    query_multiple_filter_in_one()
    print("--- query_and_() ---")
    query_and_()
    print("--- query_multiple_filter() ---")
    query_multiple_filter()
    print("--- query_or_() ---")
    query_or_()

    # Works with SQLAlchemy Core but throws an error in ORM
    # print("--- query_with_python_or_() ---")
    # query_with_python_or_()
    # print("--- query_with_python_and_fails() ---")
    # query_with_python_and_fails()