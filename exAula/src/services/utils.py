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
    with open(path, "w") as file:
        json.dump(data, file, indent=4)