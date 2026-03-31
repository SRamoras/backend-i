from fastapi import APIRouter, HTTPException, status

from api.schemas import NoteCreate, NoteRead
from api.routers.meetings import DB as MEETINGS_DB

router = APIRouter(prefix="/meetings", tags=["notes"])

NOTES_DB: dict[str, list[NoteRead]] = {}


def _require_meeting(meeting_id: str) -> None:
    if meeting_id not in MEETINGS_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")


@router.post(
    "/{meeting_id}/notes",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_note(meeting_id: str, payload: NoteCreate) -> NoteRead:
    _require_meeting(meeting_id)
    notes = NOTES_DB.setdefault(meeting_id, [])
    note = NoteRead(id=str(len(notes) + 1), **payload.model_dump())
    notes.append(note)
    return note


@router.get("/{meeting_id}/notes", response_model=list[NoteRead])
def list_notes(meeting_id: str) -> list[NoteRead]:
    _require_meeting(meeting_id)
    return NOTES_DB.get(meeting_id, [])
