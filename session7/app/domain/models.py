from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class ActionItem:
    title: str
    owner: str
    due_date: str
    id: str = field(default_factory=lambda: str(uuid4()))