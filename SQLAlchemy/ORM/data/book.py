import sqlalchemy as sa
from data.modelbase import ModelBase

class Book(ModelBase):
    __tablename__ = 'Book'
    
    id = sa.Column('Id', sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column('Title', sa.String, nullable=False)
    isbn = sa.Column('ISBN', sa.String(13), nullable=False)
    pages = sa.Column('Pages', sa.Integer)
    published_by = sa.Column('PublishedBy', sa.Integer, sa.ForeignKey('Publisher.Id'), nullable=False) 
    publisher = sa.orm.relation("Publisher", back_populates="books")
    authors = sa.orm.relation("Author", secondary='BookAuthor', back_populates="books")
    details = sa.orm.relation("BookDetails", uselist=False, back_populates="book")
    
    def __repr__(self):
        return f'<Book {self.id} ({self.title} {self.isbn}) {self.pages}>'