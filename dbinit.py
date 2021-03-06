import os
import sys
import json
import psycopg2 as dbapi2
from book import Book


def readFile():
    books = []
    with open('books.json',errors='ignore') as json_file:
        data = json.load(json_file)
        for book in data['books']["book"]:         
            books.append(Book(title=book["title"], author=book["author"], genres=book["genres"], year=book["year"], pageNumber=book["pgnum"], cover=book["cover"], description=book["description"]))
    return books

INIT_STATEMENTS = [
    "DROP TABLE IF EXISTS REVIEW",
    "DROP TABLE IF EXISTS ADMINS",
    "DROP TABLE IF EXISTS BOOKWORM",
    "DROP TABLE IF EXISTS GENRES",
    "DROP TABLE IF EXISTS BOOK",   
    "DROP TABLE IF EXISTS AUTHOR",
    

    """CREATE TABLE AUTHOR(
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    DESCRIPTION VARCHAR(2000),
    PHOTO VARCHAR(200)
    )""",

    """CREATE TABLE BOOK(
    ID SERIAL PRIMARY KEY,
    TITLE VARCHAR(80) NOT NULL,
    YR INTEGER CHECK(YR>=0 AND YR<=2019),
    AUTHORID INTEGER REFERENCES AUTHOR ON DELETE SET NULL,
    PGNUM INTEGER CHECK(PGNUM>=0),
    COVER VARCHAR(200),
    DESCRIPTION VARCHAR(2000)
    )""",
    
    """CREATE TABLE BOOKWORM(
        ID SERIAL PRIMARY KEY,
        USERNAME VARCHAR(20) UNIQUE NOT NULL,
        PASSWORD VARCHAR(100) NOT NULL,
        EMAIL VARCHAR(50) UNIQUE NOT NULL,
        PROFILEPICTURE VARCHAR(30),
        GENDER VARCHAR(10)
    )""",

    """CREATE TABLE REVIEW(
        ID SERIAL PRIMARY KEY,
        SCORE INTEGER NOT NULL CHECK(SCORE>=1 AND SCORE<=10),
        COMMENT VARCHAR(2000),
        DATEWRITTEN TIMESTAMP,
        BOOKID INTEGER REFERENCES BOOK ON DELETE CASCADE,
        USERID INTEGER REFERENCES BOOKWORM ON DELETE CASCADE
    )""",
    
    """CREATE TABLE ADMINS(
        ADMINID INTEGER UNIQUE REFERENCES BOOKWORM ON DELETE CASCADE
    )""",

    """CREATE TABLE GENRES(
        BOOKID INTEGER REFERENCES BOOK ON DELETE CASCADE,
        GENRE VARCHAR(20)
    )"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
