"""
Example for ORM part of SQLAlchemy
"""
import os
from datetime import datetime
import data.db_session as db_session
from data.employee import Employee


    
def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'mydb.sqlite')
    db_session.global_init(db_file)
    
    
def add_employee():
    employee = Employee()
    employee.last_name = "King"
    employee.first_name = "Robert"
    employee.birth_date = datetime(1990,5,29)   
    print(employee)
    
    session = db_session.factory()
    session.add(employee)
    session.commit()
    
    print(employee)
    return employee.id


def load_employee(id):
    session = db_session.factory()
    employee = session.query(Employee) \
        .filter(Employee.id == id) \
        .first()

    print(employee)
    
    session.close()    
    
    
def update_employee(id):
    session = db_session.factory()
    employee = session.query(Employee) \
        .filter(Employee.id == id) \
        .first()

    print(employee)
    
    employee.last_name = "Lord"
    
    session.commit()    
    print(employee)    


def delete_employee(id):
    session = db_session.factory()
    employee = session.query(Employee) \
        .filter(Employee.id == id) \
        .first()
    
    print(employee)
    
    session.delete(employee)
    session.commit() 

    
if __name__ == '__main__':
    print("--- setup_db() ---")
    setup_db()
    print("--- add_employee() ---")
    id = add_employee()
    print("--- load_employee() ---")
    load_employee(id)
    print("--- update_employee() ---")
    update_employee(id)
    print("--- delete_employee() ---")
    delete_employee(id)
    load_employee(id)