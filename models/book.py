class Book:
    """Represents a book in the library."""

    def __init__(self, book_id, title, author):
        self.id = book_id
        self._title = title
        self.author = author
        self.available = True

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()

    def borrow(self):
        if not self.available:
            raise ValueError("Book is already borrowed")
        self.available = False

    def return_book(self):
        if self.available:
            raise ValueError("Book is already available")
        self.available = True

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} - {status}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["id"], data["title"], data["author"])
        book.available = data["available"]
        return book