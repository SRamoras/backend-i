from uuid import uuid4
from domain.models import Meeting
from services.memory_store import meetings
from typing import Optional

def create_meeting(title: str, date: str, owner: str) -> Meeting:
    meeting = Meeting(id=str(uuid4()), title=title, date=date, owner=owner)
    meetings.append(meeting)
    return meeting


def list_meetings() -> list[Meeting]:
    return meetings


def get_meeting(meeting_id: str) -> Optional[Meeting]:
    return next((m for m in meetings if m.id == meeting_id), None)