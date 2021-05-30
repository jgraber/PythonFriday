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
        'Northwind_small.sqlite')
    db_session.global_init(db_file)
    
    
def add_employee():
    employee = Employee()
    employee.last_name = "King"
    employee.first_name = "Robert"
    employee.birth_date = '1990-05-29'   
    print(employee)
    
    session = db_session.factory()
    session.add(employee)
    session.commit()
    
    print(employee)
    return employee.id


if __name__ == '__main__':
    print("--- setup_db() ---")
    setup_db()
    print("--- add_employee() ---")
    id = add_employee()
