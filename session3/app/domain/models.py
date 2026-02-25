from dataclasses import dataclass, field
from typing import List

@dataclass
class ActionItem:
    description: str
    owner: str
    due_date: str
    status: str = "open"

@dataclass
class Meeting:
    id: str
    title: str
    date: str
    owner: str
    participants: List[str] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)