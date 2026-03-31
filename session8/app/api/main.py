from fastapi import FastAPI, HTTPException
from .models import Meeting
from datetime import datetime

api = FastAPI(title="Meeting Note Assistant API")


@api.get("/health")
def health() -> dict:
    return {"status": "ok"}


@api.get("/meetings", response_model=list[Meeting])
def list_meetings(title: str = "", owner: str = "", date: datetime | None = None) -> list:
    return []


@api.get("/meetings/{meeting_id}", response_model=Meeting)
def get_meeting(meeting_id: str):
    raise HTTPException(status_code=404, detail="Meeting not found")
