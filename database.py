from book import Book
from user import User
from review import Review
from author import Author
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
                    book.author = self.add_author(Author(name=book.author))
                else:
                    book.author = self.get_author(book.author).id
            query = "INSERT INTO BOOK (TITLE, AUTHORID, YR, PGNUM, COVER, DESCRIPTION) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID"               
            cursor.execute(query, (book.title, book.author, book.year, book.pageNumber, book.cover, book.description))
            connection.commit()
            book_id = cursor.fetchone()[0]
            for genre in book.genres:
                self.add_genre(book_id, genre)
        return book_id
    
    def update_book(self, book_id, book):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            if book.author is not None:
                if self.get_author(book.author) is None:
                    book.author = self.add_author(Author(name=book.author))
                else:
                    self.update_author(Author(name=book.author))
                    book.author = self.get_author(book.author).id
            query = "UPDATE BOOK SET TITLE = %s, AUTHORID = %s, YR = %s, PGNUM = %s, COVER = %s, DESCRIPTION = %s WHERE (ID = %s)"
            cursor.execute(query, (book.title, book.author, book.year, book.pageNumber, book.cover, book.description, book_id))
            connection.commit()
            self.delete_genres(book_id)
            for genre in book.genres:
                self.add_genre(book_id, genre)

    def delete_book(self, book_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BOOK WHERE (ID = %s)"
            cursor.execute(query, (book_id,))
            connection.commit()
            self.delete_genres(book_id)
            

    def get_book(self, book_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT TITLE, AUTHORID, YR, PGNUM, COVER, DESCRIPTION FROM BOOK WHERE (ID = %s)"
            cursor.execute(query1, (book_id,))           
            title, author_id, year, pageNumber, cover, description = cursor.fetchone()
            author = None
            if author_id:
                query2 = "SELECT NAME FROM AUTHOR WHERE (ID = %s)"
                cursor.execute(query2, (author_id,))
                author = cursor.fetchone()[0]
            query3 = "SELECT AVG(SCORE) FROM REVIEW WHERE (BOOKID = %s)"
            cursor.execute(query3, (book_id,))
            avgscore = cursor.fetchone()[0]
            genres = self.get_genres(book_id)
        book_ = Book(id=book_id, title=title, author=author, year=year, genres=genres, pageNumber=pageNumber, cover=cover, description=description, avgscore=avgscore)
        return book_, author_id

    def get_books(self, query=None, genre=None, year=None, p=None):
        books = []
        offset = (int(p) - 1) * 12 if (int(p) > 0 and p) else 0
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            if query:
                query1 = "SELECT ID, TITLE, YR, COVER FROM BOOK WHERE LOWER(TITLE) LIKE LOWER(%s) ORDER BY ID OFFSET %s LIMIT 12"
                query_words = query.split()
                like_pattern = '%'
                for word in query_words:
                    like_pattern += '{}%'.format(word)
                cursor.execute(query1, (like_pattern, offset))
            elif genre:
                query1 = "SELECT BOOK.ID, BOOK.TITLE, BOOK.YR, BOOK.COVER FROM BOOK INNER JOIN GENRES ON BOOK.ID = GENRES.BOOKID WHERE (GENRE = %s) GROUP BY BOOK.ID, BOOK.TITLE, BOOK.YR, BOOK.COVER ORDER BY BOOK.ID OFFSET %s LIMIT 12"
                cursor.execute(query1, (genre, offset))
            elif year:
                query1 = "SELECT ID, TITLE, YR, COVER FROM BOOK WHERE (YR = %s) ORDER BY ID OFFSET %s LIMIT 12"
                cursor.execute(query1, (year, offset))
            else:
                query1 = "SELECT ID, TITLE, YR, COVER FROM BOOK ORDER BY ID OFFSET %s LIMIT 12"
                cursor.execute(query1, (offset,))
            for book_id, title, year, cover in cursor:
                books.append(Book(id=book_id, title=title, year=year, cover=cover))   
        return books

    def get_books_by_author(self, author_id):
        books = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, TITLE, YR, COVER FROM BOOK WHERE (AUTHORID = %s) ORDER BY ID"
            cursor.execute(query, (author_id,))
            for book_id, title, year, cover in cursor:
                books.append(Book(id=book_id, title=title, year=year, cover=cover))   
        return books

    def get_books_count(self, query=None, year=None, genre=None):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query1 = "SELECT COUNT(ID) FROM BOOK"
            if query or year or genre:
                query1 += " WHERE "
                if query:
                    query1 += "LOWER(TITLE) LIKE LOWER(%s)"
                    cursor.execute(query1, (query,))
                elif year:
                    query1 += "(YR = %s)"
                    cursor.execute(query1, (year,))
                elif genre:
                    query1 = "SELECT COUNT(BOOK.ID) FROM BOOK INNER JOIN GENRES ON BOOK.ID = GENRES.BOOKID WHERE (GENRE = %s)"
                    cursor.execute(query1, (genre,))
            else:
                cursor.execute(query1)
            count = cursor.fetchone()[0]
        return count

    def get_top_books(self):
        books = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT BOOK.ID, BOOK.TITLE, BOOK.YR, BOOK.COVER, AVG(REVIEW.SCORE) FROM BOOK INNER JOIN REVIEW ON BOOK.ID = REVIEW.BOOKID GROUP BY BOOK.ID, BOOK.TITLE, BOOK.YR, BOOK.COVER ORDER BY AVG(REVIEW.SCORE) DESC LIMIT 10"
            cursor.execute(query)
            for book_id, title, year, cover, avgscore in cursor:
                books.append(Book(id=book_id, title=title, year=year, cover=cover, avgscore=avgscore))
        return books

    def add_user(self, user):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO BOOKWORM (USERNAME, EMAIL, PASSWORD, PROFILEPICTURE, GENDER) VALUES (%s, %s, %s, %s, %s) RETURNING ID"
            cursor.execute(query, (user.username, user.email, user.password, user.profile_picture, user.gender))
            connection.commit()
            user_key = cursor.fetchone()[0]
        return user_key

    def get_user_by_username(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, USERNAME, EMAIL, PASSWORD, PROFILEPICTURE, GENDER FROM BOOKWORM WHERE (USERNAME = %s)"
            cursor.execute(query, (username,))      
            try:
                user_id, username, email, password, profile_picture, gender = cursor.fetchone()
            except:
                return None
        is_admin = self.check_admin(user_id)
        user_ = User(username, email=email, password=password, id=user_id, profile_picture=profile_picture, gender=gender, is_admin=is_admin)
        return user_

    def get_user_by_email(self, email):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, USERNAME, EMAIL, PASSWORD, PROFILEPICTURE, GENDER FROM BOOKWORM WHERE (EMAIL = %s)"
            cursor.execute(query, (email,))   
            try:
                user_id, username, email, password, profile_picture, gender = cursor.fetchone()
            except:
                return None
        is_admin = self.check_admin(user_id)
        user_ = User(username, email=email, password=password, id=user_id, profile_picture=profile_picture, gender=gender, is_admin=is_admin)
        return user_
        
    def get_user_by_id(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, USERNAME, EMAIL, PASSWORD, PROFILEPICTURE, GENDER FROM BOOKWORM WHERE (ID = %s)"
            cursor.execute(query, (user_id,))           
            try:
                user_id, username, email, password, profile_picture, gender = cursor.fetchone()
            except:
                return None
            is_admin = self.check_admin(user_id)
            user_ = User(username, email=email, password=password, id=user_id, profile_picture=profile_picture, gender=gender, is_admin=is_admin)
        return user_

    def get_user_id(self, username):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID FROM BOOKWORM WHERE (USERNAME = %s)"
            cursor.execute(query, (username,))           
            try:
                user_id = cursor.fetchone()
            except:
                return None
        return user_id

    def add_author(self, author):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO AUTHOR (NAME, DESCRIPTION, PHOTO) VALUES (%s, %s, %s) RETURNING ID"
            cursor.execute(query, (author.name, author.description, author.photo))
            connection.commit()
            author_id = cursor.fetchone()[0]
        return author_id

    def get_author(self, name):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, DESCRIPTION, PHOTO FROM AUTHOR WHERE (NAME = %s)"
            cursor.execute(query, (name,))           
            try:
                id, description, photo = cursor.fetchone()
            except:
                return None
        return Author(name=name, id=id, description=description, photo=photo)

    def get_author_by_id(self, author_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, DESCRIPTION, PHOTO FROM AUTHOR WHERE (ID = %s)"
            cursor.execute(query, (author_id,))           
            try:
                name, description, photo = cursor.fetchone()
            except:
                return None
        return Author(name=name, id=author_id, description=description, photo=photo)

    def delete_author(self, author_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM AUTHOR WHERE (ID = %s)"
            cursor.execute(query, (author_id,))           
            connection.commit()

    def update_author(self, author):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE AUTHOR SET NAME = %s, DESCRIPTION = %s, PHOTO = %s WHERE (ID = %s)"
            cursor.execute(query, (author.name, author.description, author.photo, author.id))
            connection.commit()


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
        users = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT USERID, SCORE, COMMENT, ID, DATEWRITTEN FROM REVIEW WHERE (BOOKID = %s) ORDER BY ID"
            cursor.execute(query, (book_id,))
            connection.commit()
            for userid, score, comment, review_id, datewritten in cursor:
                pp = self.get_user_by_id(userid).profile_picture
                user_dict = {
                    "id": userid,
                    "profile_picture": pp
                }
                users.append(user_dict)
                author = self.get_user_by_id(userid).username
                reviews.append(Review(author, book_id, score, comment, review_id, datewritten))
        return reviews, users
    
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
                book_names.append(self.get_book(book_id)[0].title)
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
            query = "DELETE FROM REVIEW WHERE (ID = %s)"
            cursor.execute(query, (review_id,))           
            connection.commit()

    def update_review(self, review):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE REVIEW SET SCORE = %s, COMMENT = %s WHERE (ID = %s)"
            cursor.execute(query, (review.score, review.comment, review.id))
            connection.commit()

    def delete_user(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BOOKWORM WHERE (ID = %s)"
            cursor.execute(query, (user_id,))           
            connection.commit()

    def update_user(self, user_id, user):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE BOOKWORM SET USERNAME = %s, EMAIL = %s, PASSWORD = COALESCE(%s, PASSWORD), PROFILEPICTURE = COALESCE(%s, PROFILEPICTURE), GENDER = %s WHERE (ID = %s)"
            cursor.execute(query, (user.username, user.email, user.password, user.profile_picture, user.gender, user_id))
            connection.commit()
    
    def add_admin(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ADMINS (ADMINID) VALUES (%s)"
            cursor.execute(query, (user_id,))
            connection.commit()

    def delete_admin(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ADMINS WHERE (ADMINID = %s)"
            cursor.execute(query, (user_id,))
            connection.commit()

    def check_admin(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT ADMINID FROM ADMINS WHERE (ADMINID = %s)"
            cursor.execute(query, (user_id,))
            connection.commit()
            try:
                review_id = cursor.fetchone()[0]
                if review_id:
                    return True
            except:
                return False

    def delete_profile_picture(self, user_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE BOOKWORM SET PROFILEPICTURE = NULL WHERE (ID = %s)"
            cursor.execute(query, (user_id,))
            connection.commit()

    def add_genre(self, book_id, genre):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO GENRES (BOOKID, GENRE) VALUES (%s, %s)"
            cursor.execute(query, (book_id, genre))
            connection.commit()

    def delete_genres(self, book_id):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM GENRES WHERE (BOOKID = %s)"
            cursor.execute(query, (book_id,))
            connection.commit()
    
    def get_genres(self, book_id):
        with dbapi2.connect(self.db_url) as connection:
            genres = []
            cursor = connection.cursor()
            query = "SELECT GENRE FROM GENRES WHERE (BOOKID = %s)"
            cursor.execute(query, (book_id,))
            for genre in cursor:
                genres.append(genre[0])
            cursor.execute(query, (book_id,))
            connection.commit()
            return genres       