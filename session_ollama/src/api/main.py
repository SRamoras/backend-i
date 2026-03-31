from fastapi import FastAPI
from models.meeting_model import Meeting, MeetingSummary
from storage.meeting_storage import meeting_storage
from uuid import uuid4
from services.ollama_services import generate_summary


api = FastAPI()



@api.post("/create-meeting", response_model = MeetingSummary)
def create_meeting(meeting: Meeting):
    meeting_id = uuid4()
    summary = generate_summary(meeting)

    meeting_summary = MeetingSummary(
        id=meeting_id,
        summary=summary
    )

    meeting_storage[meeting_id] = summary
    return meeting_summary


 
@api.get("/get-meetings")
def get_meetings():
    return meeting_storage