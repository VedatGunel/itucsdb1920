import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "DROP TABLE IF EXISTS RATING",
    "DROP TABLE IF EXISTS BOOKWORM",
    "DROP TABLE IF EXISTS BOOK",
    "DROP TABLE IF EXISTS AUTHOR",

    """CREATE TABLE AUTHOR(
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(30) NOT NULL
    )""",

    """CREATE TABLE BOOK(
    ID SERIAL PRIMARY KEY,
    TITLE VARCHAR(80) NOT NULL,
    YR INTEGER,
    GENRE VARCHAR(20),
    AUTHORID INTEGER REFERENCES AUTHOR,
    PGNUM INTEGER
    )""",
    
    """CREATE TABLE BOOKWORM(
        ID SERIAL PRIMARY KEY,
        USERNAME VARCHAR(20) NOT NULL,
        PASSWORD VARCHAR(100) NOT NULL,
        EMAIL VARCHAR(50) NOT NULL
    )""",

    """CREATE TABLE REVIEW(
        ID SERIAL PRIMARY KEY,
        SCORE INTEGER NOT NULL,
        COMMENT VARCHAR(200),
        BOOKID INTEGER REFERENCES BOOK,
        USERID INTEGER REFERENCES BOOKWORM
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
