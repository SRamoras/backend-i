from fastapi import FastAPI
from models.meeting_model import Meeting
from storage.meeting_storage import meeting_storage
from uuid import uuid4



api = FastAPI()



@api.post("/create-meeting", response_model = Meeting)
def create_meeting(meeting: Meeting):
    meeting_storage[uuid4()] = meeting




@api.get("/get-meetings")
def get_meetings():
    return meeting_storage