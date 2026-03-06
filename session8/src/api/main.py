from fastapi import FastAPI
from .models import Meeting, MeetingResquest, MeetingResponse
from datetime import datetime
api = FastAPI()

@api.get("/", response_model=list[Meeting])
def list_meetings(title:str = "", owner:str = "", date:datetime | None = None) -> list:

    return []
    
@api.post("/", response_model=MeetingResponse)
def create_meetings(metting: MeetingResquest):
    ...
    

@api.get("/{metting_id}", response_model=Meeting)
def get_meeting():
    ...