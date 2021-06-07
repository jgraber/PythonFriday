import sqlalchemy as sa
from data.modelbase import ModelBase

class BookAuthor(ModelBase):
    __tablename__ = 'BookAuthor'
    
    book_id = sa.Column('BookId', sa.Integer, sa.ForeignKey('Book.Id'), primary_key=True)
    author_id = sa.Column('AuthorId', sa.Integer, sa.ForeignKey('Author.Id'), primary_key=True)
        
    def __repr__(self):
        return f'<BookAuthor {self.book_id} {self.author_id}>'
