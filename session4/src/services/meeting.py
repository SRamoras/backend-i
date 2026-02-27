from data.models import Meeting
from services import database

def create(title: str, owner: str, date: str):
    new_meeting = Meeting(
        title=title,
        owner=owner,
        date=date
    )
    database.create(meeting=new_meeting)

def list():
    ...
