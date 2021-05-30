import sqlalchemy as sa
from data.modelbase import ModelBase
import datetime

class Employee(ModelBase):
    __tablename__ = 'Employee'
    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    birth_date = sa.Column(sa.Date)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return f'<Employee {self.id} ({self.first_name} {self.last_name}) {self.birth_date}>'