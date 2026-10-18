import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def load_data(filename):
    """Load a list of records from a JSON file."""
    path = DATA_DIR / filename

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list")
            return data
    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise ValueError(f"Cannot load {filename}: {error}") from error


def save_data(filename, records):
    """Save a list of records to a JSON file."""
    path = DATA_DIR / filename
    temporary_path = path.with_suffix(".tmp")

    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    temporary_path.replace(path)