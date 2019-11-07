from book import Book


class Database:
    def __init__(self):
        self.books = {}
        self._last_book_key = 0

    def add_book(self, book):
        self._last_book_key += 1
        self.books[self._last_book_key] = book
        return self._last_book_key
    
    def update_book(self, book_key, book):
        self.books[book_key] = book

    def delete_book(self, book_key):
        if book_key in self.books:
            del self.books[book_key]

    def get_book(self, book_key):
        book = self.books.get(book_key)
        if book is None:
            return None
        book_ = Book(book.title, year=book.year)
        return book_

    def get_books(self):
        books = []
        for book_key, book in self.books.items():
            book_ = Book(book.title, year=book.year)
            books.append((book_key, book_))
        return books