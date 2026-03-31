from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field
from datetime import date
from typing import Annotated


class MeetingStatus(str, Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


# Valid status transitions
_TRANSITIONS: dict[MeetingStatus, set[MeetingStatus]] = {
    MeetingStatus.scheduled: {MeetingStatus.in_progress, MeetingStatus.cancelled},
    MeetingStatus.in_progress: {MeetingStatus.completed, MeetingStatus.cancelled},
    MeetingStatus.completed: set(),
    MeetingStatus.cancelled: set(),
}


def allowed_transitions(current: MeetingStatus) -> set[MeetingStatus]:
    return _TRANSITIONS[current]


class MeetingCreate(BaseModel):
    title: Annotated[str, Field(min_length=3, description="Meeting title (at least 3 chars)")]
    date: Annotated[date, Field(description="Meeting date (YYYY-MM-DD)")]
    owner: Annotated[str, Field(min_length=2, description="Owner name (at least 2 chars)")]
    participants: Annotated[
        list[str],
        Field(min_length=1, description="Non-empty list of participant names"),
    ]


class MeetingRead(MeetingCreate):
    id: Annotated[str, Field(description="Unique meeting identifier")]
    status: MeetingStatus = MeetingStatus.scheduled


class MeetingUpdate(BaseModel):
    """Full replacement payload for PUT — all fields required."""

    title: Annotated[str, Field(min_length=3)]
    date: date
    owner: Annotated[str, Field(min_length=2)]
    participants: Annotated[list[str], Field(min_length=1)]


class MeetingStatusUpdate(BaseModel):
    """Payload for PATCH /meetings/{id}/status."""

    status: MeetingStatus
