from fastapi import APIRouter, HTTPException, status

from api.schemas import ErrorDetail, NoteCreate, NoteRead
from api.routers.meetings import DB as MEETINGS_DB

router = APIRouter(prefix="/meetings", tags=["notes"])

NOTES_DB: dict[str, list[NoteRead]] = {}

_404_meeting = {404: {"model": ErrorDetail, "description": "Meeting not found"}}


def _require_meeting(meeting_id: str) -> None:
    if meeting_id not in MEETINGS_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")


@router.post(
    "/{meeting_id}/notes",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
    responses=_404_meeting | {422: {"model": ErrorDetail, "description": "Validation error"}},
    summary="Add a note to a meeting",
)
def create_note(meeting_id: str, payload: NoteCreate) -> NoteRead:
    _require_meeting(meeting_id)
    notes = NOTES_DB.setdefault(meeting_id, [])
    note = NoteRead(id=str(len(notes) + 1), **payload.model_dump())
    notes.append(note)
    return note


@router.get(
    "/{meeting_id}/notes",
    response_model=list[NoteRead],
    responses=_404_meeting,
    summary="List notes for a meeting",
)
def list_notes(meeting_id: str) -> list[NoteRead]:
    _require_meeting(meeting_id)
    return NOTES_DB.get(meeting_id, [])
