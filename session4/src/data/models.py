from dataclasses import dataclass

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