import json
import os
from domain.models import ActionItem

DB_FILE = "data.json"

def _load() -> list[dict]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE) as f:
        return json.load(f)

def _save(items: list[dict]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(items, f, indent=2)

def save(item: ActionItem) -> ActionItem:
    items = _load()
    items.append(item.__dict__)
    _save(items)
    return item

def find_all() -> list[ActionItem]:
    return [ActionItem(**i) for i in _load()]

def find_by_id(id: str) -> ActionItem | None:
    items = _load()
    for i in items:
        if i["id"] == id:
            return ActionItem(**i)
    return None

def delete_by_id(id: str) -> bool:
    items = _load()
    new_items = [i for i in items if i["id"] != id]
    if len(new_items) == len(items):
        return False
    _save(new_items)
    return True