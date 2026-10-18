import pytest

from models.book import Book


def test_book_starts_available():
    book = Book(1, "Python Basics", "A. Writer")
    assert book.available is True


def test_book_can_be_borrowed_and_returned():
    book = Book(1, "Python Basics", "A. Writer")
    book.borrow()
    assert book.available is False

    book.return_book()
    assert book.available is True


def test_cannot_borrow_unavailable_book():
    book = Book(1, "Python Basics", "A. Writer")
    book.borrow()

    with pytest.raises(ValueError):
        book.borrow()


def test_title_cannot_be_empty():
    book = Book(1, "Python Basics", "A. Writer")

    with pytest.raises(ValueError):
        book.title = "   "


def test_book_can_be_saved_and_loaded():
    book = Book(1, "Python Basics", "A. Writer")
    restored = Book.from_dict(book.to_dict())

    assert restored.title == book.title
    assert restored.author == book.author
    assert restored.available is True