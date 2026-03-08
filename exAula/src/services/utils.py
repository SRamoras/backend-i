import json
from pathlib import Path


def ensureJson(path: Path):
    """Ensure the JSON file exists and return its content as a list."""

    if not path.exists() or path.stat().st_size == 0:
        path.parent.mkdir(exist_ok=True)
        path.write_text("[]")
    with open(path, "r") as file:
        return json.load(file)


def saveJson(path: Path, data):
    """Save a Python list to a JSON file."""

    path.parent.mkdir(exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


def handle_error(func) -> None:
    """
    Executes a function and catches ValueError exceptions.

    If a ValueError occurs, the error message is printed in a user-friendly way.
    This avoids repeating try/except blocks in every CLI command.
    """

    try:
        func()
    except ValueError as e:
        print(f"❌ {e}")