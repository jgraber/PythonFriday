import sqlalchemy as sa
from data.modelbase import ModelBase

class BookDetails(ModelBase):
    __tablename__ = 'BookDetail'
    
    book_id = sa.Column('Id', sa.Integer, sa.ForeignKey('Book.Id'), primary_key=True)
    cover = sa.Column('Cover', sa.String)
    book = sa.orm.relationship("Book", back_populates="details")
   
    
    def __repr__(self):
        return f'<BookDetails {self.book_id} ({self.cover})>'
    