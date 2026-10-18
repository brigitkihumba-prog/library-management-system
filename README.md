# Library Management System

## Group 8

A Python command-line application for managing library books, borrowers, and borrowing records.

## Problem Statement

Small libraries may use paper records or spreadsheets to track books and borrowers. This can cause missing records, confusion about available books, and difficulty tracking returns.

Our application keeps book, user, and loan records in JSON files.

## Target Users

- **Admin:** Adds, edits, removes, and lists books and manages borrower records.
- **Borrower:** Searches for books, borrows and returns books, and views personal borrowing history.

## Features

- User registration and login
- Password hashing
- Admin and Borrower roles
- Book management
- Member management
- Book search
- Borrowing and returns
- JSON file persistence
- Input validation and error handling
- Unit tests

## Technologies

- Python 3.10+
- Rich
- Pytest
- JSON
- Git and GitHub

## Project Structure

- `main.py` - CLI entry point
- `models/` - Person, User, Book, and Loan classes
- `utils/` - Authentication and JSON storage
- `data/` - JSON records
- `tests/` - Unit tests

## Installation

1. Clone the repository.
2. Enter the project directory.
3. Create and activate a virtual environment.
4. Install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Running the Application

Start the interactive menu:

```bash
python main.py
```

Or use the available commands:

```bash
python main.py --help
python main.py menu
python main.py list-books
python main.py search-book
```

The first registered account receives the Admin role. Later accounts receive the Borrower role.

## Running Tests

```bash
python -m pytest -v
```

## Storage

The application stores users, books, and loans in JSON files under `data/`.

## Known Limitations

- This is a local JSON-based application rather than a networked database.
- The CLI is designed for a single running instance at a time.
- The first registered account becomes Admin.
- Borrowing due dates, automatic fines, and simultaneous multi-user access are not implemented.

## Group Members

- Tony Toroitich
- Taby Thiongo
- Brigit Kihumba
- Catherine Kyalo

## License

Educational group project, 2026.