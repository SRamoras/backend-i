from fastapi import APIRouter, HTTPException, status
from uuid import uuid4

from api.schemas import (
    MeetingCreate,
    MeetingRead,
    MeetingUpdate,
    MeetingStatusUpdate,
    MeetingStatus,
    allowed_transitions,
)

router = APIRouter(prefix="/meetings", tags=["meetings"])

# In-memory store: { id: MeetingRead }
DB: dict[str, MeetingRead] = {}


@router.post("", response_model=MeetingRead, status_code=status.HTTP_201_CREATED)
def create_meeting(payload: MeetingCreate) -> MeetingRead:
    meeting = MeetingRead(id=str(uuid4()), **payload.model_dump())
    DB[meeting.id] = meeting
    return meeting


@router.get("", response_model=list[MeetingRead])
def list_meetings() -> list[MeetingRead]:
    return list(DB.values())


@router.get("/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: str) -> MeetingRead:
    meeting = DB.get(meeting_id)
    if meeting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return meeting


# Exercise: PUT /meetings/{id} with basic validation
@router.put("/{meeting_id}", response_model=MeetingRead)
def update_meeting(meeting_id: str, payload: MeetingUpdate) -> MeetingRead:
    meeting = DB.get(meeting_id)
    if meeting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    updated = MeetingRead(id=meeting_id, status=meeting.status, **payload.model_dump())
    DB[meeting_id] = updated
    return updated


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meeting(meeting_id: str) -> None:
    if meeting_id not in DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    del DB[meeting_id]


# Challenge: PATCH /meetings/{id}/status with transition rules
@router.patch("/{meeting_id}/status", response_model=MeetingRead)
def update_meeting_status(meeting_id: str, payload: MeetingStatusUpdate) -> MeetingRead:
    meeting = DB.get(meeting_id)
    if meeting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    allowed = allowed_transitions(meeting.status)
    if payload.status not in allowed:
        if not allowed:
            detail = f"Meeting is already in terminal status '{meeting.status}', no transitions allowed."
        else:
            allowed_names = ", ".join(s.value for s in allowed)
            detail = (
                f"Cannot transition from '{meeting.status}' to '{payload.status}'. "
                f"Allowed transitions: {allowed_names}."
            )
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=detail)

    meeting.status = payload.status
    DB[meeting_id] = meeting
    return meeting
