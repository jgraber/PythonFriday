from sqlalchemy import MetaData, Table, Column, String, Integer, text, DateTime, Boolean, create_engine, select, insert, update, delete, or_, and_
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint

connection_string = "sqlite:///Bookstore.sqlite"

engine = create_engine(connection_string)
metadata = MetaData()

publishers = Table('Publisher', metadata,
                 Column('Id', Integer(), primary_key=True),
                 Column('Name', String(200)),
)

books = Table('Book', metadata,
                 Column('Id', Integer(), primary_key=True),
                 Column('Title', String(8000)),
                 Column('ISBN', String(13)),
                 Column('Pages', Integer()),
                 Column('PublishedBy', Integer(), ForeignKey('Publisher.Id'), nullable=False), 
)

bookdetails = Table('BookDetail', metadata,
                 Column('Id', ForeignKey('Book.Id'), primary_key=True ),
                 Column('Cover', String(8000))
)

authors = Table('Author', metadata,
                 Column('Id', Integer(), primary_key=True),
                 Column('LastName', String(8000)),
                 Column('FirstName', String(13)),
)

book_authors = Table('BookAuthor', metadata,
                 Column('BookId', ForeignKey('Book.Id')),
                 Column('AuthorId', ForeignKey('Author.Id')),
                 PrimaryKeyConstraint('BookId', 'AuthorId',
                                 name='BookAuthor_pk')
)

metadata.create_all(engine)


def print_result(stmt):
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        rs = con.execute(stmt)
        for row in rs:
            print(row) 


def create_publisher(name):
    stmt = insert(publishers).values(
        Name=name)
    
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        result = con.execute(stmt)
        new_id = result.inserted_primary_key[0]
        pub = select(publishers).where(publishers.c.Id == new_id)
        return con.execute(pub).first() 
    
    
def create_book(title, isbn, pages, publisher):
    stmt = insert(books).values(
        Title=title,
        ISBN=isbn,
        Pages=pages,
        PublishedBy=publisher.Id)
    
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(text('PRAGMA foreign_keys=on'))
        result = con.execute(stmt)
        new_id = result.inserted_primary_key[0]
        book = select(books).where(books.c.Id == new_id)
        return con.execute(book).first() 


def create_author(first, last):
    stmt = insert(authors).values(
        FirstName=first,
        LastName=last)
    
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(text('PRAGMA foreign_keys=on'))
        result = con.execute(stmt)
        new_id = result.inserted_primary_key[0]
        author = select(authors).where(authors.c.Id == new_id)
        return con.execute(author).first() 


def create_book_author(book, author):
    stmt = insert(book_authors).values(
        BookId=book.Id,
        AuthorId=author.Id)
    
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(text('PRAGMA foreign_keys=on'))
        result = con.execute(stmt)
        bookauthor = select(book_authors).where((book_authors.c.BookId == book.Id) & (book_authors.c.AuthorId == author.Id) )
        return con.execute(bookauthor).first() 


def create_book_details(book):
    stmt = insert(bookdetails).values(
        Id=book.Id,
        Cover='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1309305569l/477597.jpg')
    
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(text('PRAGMA foreign_keys=on'))
        result = con.execute(stmt)
        new_id = result.inserted_primary_key[0]
        details = select(bookdetails).where(bookdetails.c.Id == new_id)
        return con.execute(details).first() 


def show_book_and_publisher():
    manning = create_publisher("Manning Publications")
    bookA = create_book("The Mikado Method", "9781617291210", 245, manning)
    bookB = create_book("Specification by Example", "9781617290084", 249, manning)
    
    print(manning)
    print(bookA)
    print(bookB)
    
    join_publisher_books = publishers.join(books, publishers.c.Id == books.c.PublishedBy)
    print(join_publisher_books)
    
    stmt = select(publishers, books).\
            select_from(join_publisher_books).\
            where(publishers.c.Id == manning.Id)
            
    print_result(stmt)
    
    stmt = select(books.c.Title, books.c.ISBN, books.c.Pages, publishers.c.Name).\
            select_from(join_publisher_books).\
            where(publishers.c.Id == manning.Id)
            
    print_result(stmt)



def show_authors_of_book():
    manning = create_publisher("Manning Publications")
    bookA = create_book("The Mikado Method", "9781617291210", 245, manning)
    bookB = create_book("Specification by Example", "9781617290084", 249, manning)
    
    authorA = create_author("Ola", "Ellnestam")
    authorB = create_author("Daniel", "Brolund")
    authorC = create_author("Gojko", "Adzic")

    create_book_author(bookA, authorA)
    create_book_author(bookA, authorB)
    create_book_author(bookB, authorC)
    
    join_book_authors = book_authors.\
        join(books).\
        join(authors)
    
    print(join_book_authors)

    stmt = select(books.c.Title, authors).\
            select_from(join_book_authors).\
            where(book_authors.c.BookId == bookA.Id)
            
    print_result(stmt)


def show_left_outer_join():
    manning = create_publisher("Manning Publications")
    harper = create_publisher("Harper Collins")
    bookA = create_book("The Mikado Method", "9781617291210", 245, manning)
    
    join_publisher_books = publishers.join(books)
    print(join_publisher_books)
    
    stmt = select(publishers, books).\
            select_from(join_publisher_books)
            
    print_result(stmt)
    
    join_publisher_books_full = publishers.join(books, isouter=True)
    print(join_publisher_books_full)
    
    stmt = select(publishers, books).\
            select_from(join_publisher_books_full)
            
    print_result(stmt)
    

if __name__ == '__main__':
    print("\n---- show_book_and_publisher() ----")  
    show_book_and_publisher()
    print("\n---- show_authors_of_book() ----")  
    show_authors_of_book()
    print("\n---- show_left_outer_join() ----")  
    show_left_outer_join()
