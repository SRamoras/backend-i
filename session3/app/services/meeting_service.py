from uuid import uuid4
from domain.models import Meeting
from services.memory_store import meetings


def create_meeting(title: str, date: str, owner: str) -> Meeting:
    meeting = Meeting(id=str(uuid4()), title=title, date=date, owner=owner)
    meetings.append(meeting)
    return meeting


def list_meetings() -> list[Meeting]:
    return meetings

def show_meeting(meeting_id: str) -> Meeting:
    for meeting in meetings:
        if meeting.id == meeting_id:
            return meeting
        else: 
            return "Meeting not found"