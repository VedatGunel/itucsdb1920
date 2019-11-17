from book import Book
import psycopg2 as dbapi2

class Database:
    def __init__(self, db_url):
        self.books = {}
        self.db_url = db_url

    def add_book(self, book):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO BOOK (TITLE, AUTHOR, GENRE, YR, PGNUM) VALUES (%s, %s, %s, %s, %s) RETURNING ID"
            cursor.execute(query, (book.title, book.author, book.genre, book.year, book.pageNumber))
            connection.commit()
            book_key = cursor.fetchone()[0]
        return book_key
    
    def update_book(self, book_key, book):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE BOOK SET TITLE = %s, AUTHOR = %s, GENRE = %s, YR = %s, PGNUM = %s WHERE (ID = %s)"
            cursor.execute(query, (book.title, book.author, book.genre, book.year, book.pageNumber, book_key))
            connection.commit()

    def delete_book(self, book_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BOOK WHERE (ID = %s)"
            cursor.execute(query, (book_key,))
            connection.commit()

    def get_book(self, book_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, AUTHOR, GENRE, YR, PGNUM FROM BOOK WHERE (ID = %s)"
            cursor.execute(query, (book_key,))           
            try:
                title, author, genre, year, pageNumber = cursor.fetchone()
            except TypeError:
                return None
        book_ = Book(title, author=author, genre=genre, year=year, pageNumber=pageNumber)
        return book_

    def get_books(self):
        books = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, TITLE, AUTHOR, GENRE, YR, PGNUM FROM BOOK ORDER BY ID"
            cursor.execute(query)
            for book_key, title, author, genre, year, pageNumber in cursor:
                books.append((book_key, Book(title, author, genre, year, pageNumber)))
        return books