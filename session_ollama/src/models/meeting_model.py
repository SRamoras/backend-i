from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class Meeting(BaseModel):
    name:str
    owner:str
    date:datetime
    notes:str

class MeetingSummary(BaseModel):
    id:UUID
    summary:str