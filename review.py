class Review:
    def __init__(self, author, book, score=None, comment=None, id=None, datewritten=None):
        self.author = author
        self.book = book
        self.score = score
        self.comment = comment
        self.id = id
        self.datewritten = datewritten