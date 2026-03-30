from dataclasses import dataclass, field

@dataclass
class ActionItem:
    description: str
    owner: str
    due_date: str
    status: str = "open"

@dataclass
class Meeting:
    title: str
    owner: str
    date: str
    participants: list[str] = field(default_factory=list)
    action_items: list[ActionItem] = field(default_factory=list)

    def __str__(self):
        return f"""---
title: {self.title}
owner: {self.owner}
date: {self.date}
participants: {', '.join(self.participants)}
---
# Meeting
"""

@dataclass
class MeetingData:
    metting: Meeting
    path: str