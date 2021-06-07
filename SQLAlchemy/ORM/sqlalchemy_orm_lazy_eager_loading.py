import os
from datetime import datetime

from sqlalchemy.orm import joinedload, selectinload
import data.db_session as db_session
from data.__all_models import Book, Publisher, Author, BookDetails
from sqlalchemy import or_, and_
    
def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'Bookstore.sqlite')
    db_session.global_init(db_file)
    
def create_publisher(name):
    publisher = Publisher()
    publisher.name = name

    return publisher


def create_book(title, isbn, pages, publisher):
    book = Book()
    book.title = title
    book.isbn = isbn
    book.pages = pages
    book.publisher = publisher
        
    return book


def create_author(first, last):
    author = Author()
    author.first_name = first
    author.last_name = last
    
    return author

def  create_book_details(cover, book):
    details = BookDetails()
    details.book = book
    details.cover = cover
    
    return details


def create_publisher_with_3_books():
    session = db_session.factory()
    manning = create_publisher("Manning Publications")
    session.add(manning)
    
    bookA = create_book("The Mikado Method", "9781617291210", 245, manning)
    session.add(bookA)
    
    bookB = create_book("Specification by Example", "9781617290084", 249, manning)
    session.add(bookB)
    
    bookC = create_book("Python Workout", "9781617295508", 248, manning)
    session.add(bookC)
    
    authorA = create_author("Ola", "Ellnestam")
    session.add(authorA)
    
    authorB = create_author("Daniel", "Brolund")
    session.add(authorB)
    
    authorC = create_author("Gojko", "Adzic")
    session.add(authorC)
    
    authorD = create_author("Reuven M.", "Lerner")
    session.add(authorD)
    
    bookA.authors.append(authorA)
    bookA.authors.append(authorB)
    bookB.authors.append(authorC)
    bookC.authors.append(authorD)
    
    session.commit()
    return manning.id


def lazy_loading_works_while_session_open(publisher_id):
    session = db_session.factory()
    publisher = session.query(Publisher).\
        filter(Publisher.id == publisher_id).\
        first()
        
    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t {book}:")
        for author in book.authors:
            print(f"\t\t {author}")

    session.close()
    

def lazy_loading_throws_error(publisher_id):
    session = db_session.factory()
    publisher = session.query(Publisher).\
        filter(Publisher.id == publisher_id).\
        first()
    session.close()
    
    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t {book}:")
        for author in book.authors:
            print(f"\t\t {author}")


def eager_loading_joinedload(publisher_id):
    session = db_session.factory()
    publisher = session.query(Publisher).\
        options(joinedload("books").\
        joinedload("authors")).\
        filter(Publisher.id == publisher_id).\
        first()
    session.close()
    
    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t {book}:")
        for author in book.authors:
            print(f"\t\t {author}")
 
 
def eager_loading_selectinload(publisher_id):
    session = db_session.factory()
    publisher = session.query(Publisher).\
        options(selectinload("books").\
        selectinload("authors")).\
        filter(Publisher.id == publisher_id).\
        first()
    session.close()
    
    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t {book}:")
        for author in book.authors:
            print(f"\t\t {author}")               


if __name__ == '__main__':
    print("\n--- setup_db() ---\n")
    setup_db()
    
    print("\n--- create_publisher_with_3_books() ---\n")
    publisher_id = create_publisher_with_3_books()
    
    print("\n--- lazy_loading_works_while_session_open() ---\n")
    lazy_loading_works_while_session_open(publisher_id)
    
    print("\n--- lazy_loading_throws_error() ---\n")
    try:
        lazy_loading_throws_error(publisher_id)
    except Exception as error:
        print(f"{type(error)}: {error}")
        
    print("\n--- eager_loading_joinedload() ---\n")    
    eager_loading_joinedload(publisher_id)
    
    print("\n--- eager_loading_selectinload() ---\n")    
    eager_loading_selectinload(publisher_id)