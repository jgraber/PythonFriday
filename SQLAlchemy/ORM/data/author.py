import sqlalchemy as sa
from data.modelbase import ModelBase

class Author(ModelBase):
    __tablename__ = 'Author'
    
    id = sa.Column('Id', sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column('FirstName', sa.String, nullable=False)
    last_name = sa.Column('LastName', sa.String, nullable=False)
    books = sa.orm.relation("Book", secondary='BookAuthor', back_populates="authors")
    
    def __repr__(self):
        return f'<Author {self.id} ({self.first_name} {self.last_name})>'