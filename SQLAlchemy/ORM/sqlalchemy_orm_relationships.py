import os
from datetime import datetime
import data.db_session as db_session
from data.__all_models import Book, Publisher
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
    # book.published_by = publisher.id
    book.publisher = publisher

    
    return book


def show_book_and_publisher():
    session = db_session.factory()
    manning = create_publisher("Manning Publications")
    session.add(manning)
    print(manning)
    
    bookA = create_book("The Mikado Method", "9781617291210", 245, manning)
    session.add(bookA)
    print(bookA)
    
    bookB = create_book("Specification by Example", "9781617290084", 249, manning)
    session.add(bookB)
    print(bookB)
    
    session.commit()
    
    print(manning)
    print(bookA)
    print(bookB)   
    
    print("\n-----\n")
    
    publisher = session.query(Publisher).filter(Publisher.id == manning.id).first()
    for b in publisher.books:
        print(f"{b.title} publiyhed by {b.publisher}")
    

if __name__ == '__main__':
    print("--- setup_db() ---")
    setup_db()
    print("--- show_book_and_publisher() ---")
    show_book_and_publisher()