from fastapi import APIRouter, HTTPException, status

from api.schemas import DecisionCreate, DecisionRead
from api.routers.meetings import DB as MEETINGS_DB

router = APIRouter(prefix="/meetings", tags=["decisions"])

DECISIONS_DB: dict[str, list[DecisionRead]] = {}


def _require_meeting(meeting_id: str) -> None:
    if meeting_id not in MEETINGS_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")


@router.post(
    "/{meeting_id}/decisions",
    response_model=DecisionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_decision(meeting_id: str, payload: DecisionCreate) -> DecisionRead:
    _require_meeting(meeting_id)
    decisions = DECISIONS_DB.setdefault(meeting_id, [])
    decision = DecisionRead(id=str(len(decisions) + 1), **payload.model_dump())
    decisions.append(decision)
    return decision


@router.get("/{meeting_id}/decisions", response_model=list[DecisionRead])
def list_decisions(meeting_id: str) -> list[DecisionRead]:
    _require_meeting(meeting_id)
    return DECISIONS_DB.get(meeting_id, [])
