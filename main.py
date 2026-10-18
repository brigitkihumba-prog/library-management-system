import argparse
from getpass import getpass

from rich.console import Console
from rich.table import Table

from models.user import User
from models.book import Book
from models.loan import Loan
from utils.storage import load_data, save_data
from utils.auth import hash_password, verify_password, requires_role

console = Console()


def load_users():
    return [User.from_dict(item) for item in load_data("users.json")]


def load_books():
    return [Book.from_dict(item) for item in load_data("books.json")]


def load_loans():
    return [Loan.from_dict(item) for item in load_data("loans.json")]


def next_id(items):
    return max((item.id for item in items), default=0) + 1


def register():
    users = load_users()
    name = input("Name: ").strip()
    email = input("Email: ").strip().lower()

    if not name or not email or "@" not in email:
        print("Enter a valid name and email.")
        return

    if any(user.email == email for user in users):
        print("That email is already registered.")
        return

    password = getpass("Password: ")
    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    role = "admin" if not users else "borrower"

    user = User(
        next_id(users), name, email, hash_password(password), role
    )
    users.append(user)
    save_data("users.json", [item.to_dict() for item in users])

    print(f"Registration successful. Your role is {role}.")


def login():
    users = load_users()
    email = input("Email: ").strip().lower()
    password = getpass("Password: ")

    for user in users:
        if user.email == email and verify_password(
            password, user.password_hash
        ):
            print(f"Welcome, {user.name}!")
            return user

    print("Incorrect email or password.")
    return None


def show_books():
    books = load_books()
    table = Table(title="Library Books")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Status")

    for book in books:
        status = "Available" if book.available else "Borrowed"
        table.add_row(str(book.id), book.title, book.author, status)

    console.print(table)


def search_book():
    keyword = input("Enter a title to search: ").strip().lower()
    books = load_books()
    matches = [book for book in books if keyword in book.title.lower()]

    if not matches:
        print("No matching books found.")
        return

    for book in matches:
        print(book)


@requires_role("admin")
def add_book(current_user):
    books = load_books()
    title = input("Book title: ").strip()
    author = input("Author: ").strip()

    if not title or not author:
        print("Title and author are required.")
        return

    book = Book(next_id(books), title, author)
    books.append(book)
    save_data("books.json", [item.to_dict() for item in books])
    print("Book added successfully.")


@requires_role("admin")
def edit_book(current_user):
    books = load_books()
    try:
        book_id = int(input("Book ID to edit: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    for book in books:
        if book.id == book_id:
            title = input("New title: ").strip()
            author = input("New author: ").strip()

            if not title or not author:
                print("Title and author are required.")
                return

            book.title = title
            book.author = author
            save_data("books.json", [item.to_dict() for item in books])
            print("Book updated.")
            return

    print("Book not found.")


@requires_role("admin")
def remove_book(current_user):
    books = load_books()
    loans = load_loans()

    try:
        book_id = int(input("Book ID to remove: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    if any(
        loan.book_id == book_id and loan.returned_at is None
        for loan in loans
    ):
        print("Return the book before removing it.")
        return

    updated_books = [book for book in books if book.id != book_id]

    if len(updated_books) == len(books):
        print("Book not found.")
        return

    save_data("books.json", [item.to_dict() for item in updated_books])
    print("Book removed.")


@requires_role("admin")
def list_members(current_user):
    users = load_users()

    for user in users:
        print(f"{user.id}: {user.name} - {user.email} ({user.role})")


@requires_role("admin")
def remove_member(current_user):
    users = load_users()
    loans = load_loans()

    try:
        user_id = int(input("Member ID to remove: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    member = next(
        (user for user in users if user.id == user_id), None
    )

    if member is None or member.role == "admin":
        print("Borrower not found.")
        return

    if any(
        loan.user_id == user_id and loan.returned_at is None
        for loan in loans
    ):
        print("This borrower has an active loan.")
        return

    users = [user for user in users if user.id != user_id]
    save_data("users.json", [item.to_dict() for item in users])
    print("Borrower removed.")


@requires_role("borrower")
def borrow_book(current_user):
    books = load_books()
    loans = load_loans()

    try:
        book_id = int(input("Book ID to borrow: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    book = next((item for item in books if item.id == book_id), None)

    if book is None:
        print("Book not found.")
        return

    if not book.available:
        print("Book is already borrowed.")
        return

    book.borrow()
    loan = Loan(next_id(loans), current_user.id, book.id)
    loans.append(loan)

    save_data("books.json", [item.to_dict() for item in books])
    save_data("loans.json", [item.to_dict() for item in loans])
    print("Book borrowed successfully.")


@requires_role("borrower")
def return_book(current_user):
    books = load_books()
    loans = load_loans()

    try:
        book_id = int(input("Book ID to return: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    loan = next(
        (
            item for item in loans
            if item.user_id == current_user.id
            and item.book_id == book_id
            and item.returned_at is None
        ),
        None,
    )

    if loan is None:
        print("You do not have this book on loan.")
        return

    book = next((item for item in books if item.id == book_id), None)

    if book is None:
        print("Book record not found.")
        return

    loan.return_book()
    book.return_book()

    save_data("books.json", [item.to_dict() for item in books])
    save_data("loans.json", [item.to_dict() for item in loans])
    print("Book returned successfully.")


@requires_role("borrower")
def borrowing_history(current_user):
    loans = load_loans()
    books = load_books()

    history = [
        loan for loan in loans if loan.user_id == current_user.id
    ]

    if not history:
        print("You have no borrowing history.")
        return

    for loan in history:
        book = next(
            (item for item in books if item.id == loan.book_id), None
        )
        title = book.title if book else "Removed book"
        status = "Returned" if loan.returned_at else "Not returned"
        print(f"{title}: {loan.borrowed_at} - {status}")


def menu():
    current_user = None

    while True:
        print("\n=== Library Management System ===")
        print("1. Register")
        print("2. Login")
        print("3. List books")
        print("4. Search book")
        print("5. Add book (Admin)")
        print("6. Edit book (Admin)")
        print("7. Remove book (Admin)")
        print("8. List members (Admin)")
        print("9. Remove member (Admin)")
        print("10. Borrow book (Borrower)")
        print("11. Return book (Borrower)")
        print("12. My borrowing history (Borrower)")
        print("13. Logout")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                register()
            elif choice == "2":
                current_user = login()
            elif choice == "3":
                show_books()
            elif choice == "4":
                search_book()
            elif choice == "5":
                add_book(current_user)
            elif choice == "6":
                edit_book(current_user)
            elif choice == "7":
                remove_book(current_user)
            elif choice == "8":
                list_members(current_user)
            elif choice == "9":
                remove_member(current_user)
            elif choice == "10":
                borrow_book(current_user)
            elif choice == "11":
                return_book(current_user)
            elif choice == "12":
                borrowing_history(current_user)
            elif choice == "13":
                current_user = None
                print("Logged out.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except (PermissionError, ValueError) as error:
            print(error)


def main():
    parser = argparse.ArgumentParser(
        description="Library Management System"
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("menu", help="Open the interactive menu")
    subparsers.add_parser("list-books", help="List all books")
    subparsers.add_parser("search-book", help="Search books by title")

    args = parser.parse_args()

    if args.command in (None, "menu"):
        menu()
    elif args.command == "list-books":
        show_books()
    elif args.command == "search-book":
        search_book()


if __name__ == "__main__":
    main()