from datetime import datetime


class Loan:
    """Records a book borrowed by a user."""

    def __init__(self, loan_id, user_id, book_id):
        self.id = loan_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrowed_at = datetime.now().isoformat(timespec="seconds")
        self.returned_at = None

    def return_book(self):
        if self.returned_at is not None:
            raise ValueError("Book has already been returned")
        self.returned_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "borrowed_at": self.borrowed_at,
            "returned_at": self.returned_at,
        }

    @classmethod
    def from_dict(cls, data):
        loan = cls(data["id"], data["user_id"], data["book_id"])
        loan.borrowed_at = data["borrowed_at"]
        loan.returned_at = data["returned_at"]
        return loan