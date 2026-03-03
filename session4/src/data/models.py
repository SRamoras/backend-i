from dataclasses import dataclass, asdict
import json

@dataclass
class Meeting:
    title: str
    owner: str
    date: str

    def __str__(self):
        return f"""---
title: {self.title}
owner: {self.owner}
date: {self.date}
---
# Meeting
"""


@dataclass
class MeetingData:
    metting: Meeting
    path: str
