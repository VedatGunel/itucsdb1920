from book import Book
from user import User
from review import Review
import time
import psycopg2 as dbapi2

class Database:
    def __init__(self, db_url):
        self.db_url = db_url

    def add_book(self, book):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            if book.author is not None:
                if self.get_author(book.author) is None:
                    book.author = self.add_author(book.author)
                else:
                    book.author = self.get_author(book.author)
            query2 = "INSERT INTO BOOK (TITLE, AUTHORID, GENRE, YR, PGNUM, COVER) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID"
            cursor.execute(query2, (book.title, book.author, book.genre, book.year, book.pageNumber, book.cover))
            connection.commit()
            book_id = cursor.fetchone()[0]
        return book_id
    
    def update_book(self, book_id, book):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            if book.author is not None:
                if self.get_author(book.author) is None:
                    book.author = self.add_author(book.author)
                else:
                    book.author = self.get_author(book.author)
            query2 = "UPDATE BOOK SET TITLE = %s, AUTHORID = %s, GENRE = %s, YR = %s, PGNUM = %s, COVER = %s WHERE (ID = %s)"
            cursor.execute(query2, (book.title, book.author, book.genre, book.year, book.pageNumber, book.cover, book_id))
            connection.commit()

    def delete_book(self, book_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BOOK WHERE (ID = %s)"
            cursor.execute(query, (book_id,))
            connection.commit()

    def get_book(self, book_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT TITLE, AUTHORID, GENRE, YR, PGNUM, COVER FROM BOOK WHERE (ID = %s)"
            cursor.execute(query1, (book_id,))           
            title, author, genre, year, pageNumber, cover = cursor.fetchone()
            query2 = "SELECT NAME FROM AUTHOR WHERE (ID = %s)"
            cursor.execute(query2, (author,))
            author = cursor.fetchone()[0]
            query3 = "SELECT AVG(SCORE) FROM REVIEW WHERE (BOOKID = %s)"
            cursor.execute(query3, (book_id,))
            avgscore = cursor.fetchone()[0]
        book_ = Book(id=book_id, title=title, author=author, genre=genre, year=year, pageNumber=pageNumber, cover=cover, avgscore=avgscore)
        return book_

    def get_books(self):
        books = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT ID, TITLE, YR, COVER FROM BOOK ORDER BY ID"
            cursor.execute(query1)
            for book_id, title, year, cover in cursor:
                books.append(Book(id=book_id, title=title, year=year, cover=cover))   
        return books
    

    def add_user(self, user):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO BOOKWORM (USERNAME, EMAIL, PASSWORD) VALUES (%s, %s, %s) RETURNING ID"
            cursor.execute(query, (user.username, user.email, user.password))
            connection.commit()
            user_key = cursor.fetchone()[0]
        return user_key

    def get_user_by_username(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, USERNAME, EMAIL, PASSWORD FROM BOOKWORM WHERE (USERNAME = %s)"
            cursor.execute(query, (username,))      
            try:
                user_id, username, email, password = cursor.fetchone()
            except:
                return None
        user_ = User(username, email=email, password=password, id=user_id)
        return user_

    def get_user_by_email(self, email):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, USERNAME, EMAIL, PASSWORD FROM BOOKWORM WHERE (EMAIL = %s)"
            cursor.execute(query, (email,))   
            try:
                user_id, username, email, password = cursor.fetchone()
            except:
                return None
        user_ = User(username, email=email, password=password, id=user_id)
        return user_
        
    def get_user_by_id(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT ID, USERNAME, EMAIL, PASSWORD FROM BOOKWORM WHERE (ID = %s)"
            cursor.execute(query1, (user_id,))           
            try:
                user_id, username, email, password = cursor.fetchone()
            except:
                return None
            user_ = User(username, email=email, password=password, id=user_id)
        return user_

    def get_user_id(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT ID FROM BOOKWORM WHERE (USERNAME = %s)"
            cursor.execute(query1, (username,))           
            try:
                user_id = cursor.fetchone()
            except:
                return None
        return user_id

    def add_author(self, name):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO AUTHOR (NAME) VALUES (%s) RETURNING ID"
            cursor.execute(query, (name,))
            connection.commit()
            author_id = cursor.fetchone()[0]
        return author_id

    def get_author(self, name):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT ID FROM AUTHOR WHERE (NAME = %s)"
            cursor.execute(query1, (name,))           
            try:
                id = cursor.fetchone()
            except:
                return None
        return id

    def add_review(self, review):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO REVIEW (SCORE, COMMENT, BOOKID, USERID, DATEWRITTEN) VALUES (%s, %s, %s, %s, %s) RETURNING ID"
            cursor.execute(query, (review.score, review.comment, review.book, review.author, time.strftime('%Y-%m-%d %H:%M')))
            connection.commit()
            review_id = cursor.fetchone()[0]
        return review_id

    def get_reviews(self, book_id):
        reviews = []
        user_ids = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT USERID, SCORE, COMMENT, ID, DATEWRITTEN FROM REVIEW WHERE (BOOKID = %s) ORDER BY ID"
            cursor.execute(query, (book_id,))
            connection.commit()
            for userid, score, comment, review_id, datewritten in cursor:
                user_ids.append(userid)
                author = self.get_user_by_id(userid).username
                reviews.append(Review(author, book_id, score, comment, review_id, datewritten))
        return reviews, user_ids
    
    def get_reviews_by_user(self, user_id):
        reviews = []
        book_names = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT BOOKID, SCORE, COMMENT, ID, DATEWRITTEN FROM REVIEW WHERE (USERID = %s) ORDER BY ID"
            cursor.execute(query, (user_id,))
            connection.commit()           
            for book_id, score, comment, review_id, datewritten in cursor:
                author = self.get_user_by_id(user_id).username
                book_names.append(self.get_book(book_id).title)
                reviews.append(Review(author, book_id, score, comment, review_id, datewritten))
        return reviews, book_names

    def get_review(self, review_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT USERID, BOOKID, SCORE, COMMENT, DATEWRITTEN FROM REVIEW WHERE (ID = %s)"
            cursor.execute(query1, (review_id,))           
            user_id, book_id, score, comment, datewritten = cursor.fetchone()
        review_ = Review(author=user_id, book=book_id, score=score, comment=comment, id=review_id, datewritten=datewritten)
        return review_

    def delete_review(self, review_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "DELETE FROM REVIEW WHERE (ID = %s)"
            cursor.execute(query1, (review_id,))           
            connection.commit()