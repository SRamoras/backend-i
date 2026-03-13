from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Meeting(BaseModel):
    title: str
    owner: str
    date: datetime
    content: str


class MeetingResquest(BaseModel):
    title: str
    owner: str
    content: str

class MeetingResponse(BaseModel):
    id: UUID