from __future__ import annotations

from enum import Enum
from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, model_validator


# ── Meetings ──────────────────────────────────────────────────────────────────

class MeetingStatus(str, Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


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
    title: Annotated[str, Field(min_length=3)]
    date: date
    owner: Annotated[str, Field(min_length=2)]
    participants: Annotated[list[str], Field(min_length=1)]


class MeetingStatusUpdate(BaseModel):
    status: MeetingStatus


class MeetingListResponse(BaseModel):
    total: int
    items: list[MeetingRead]


# ── Notes ─────────────────────────────────────────────────────────────────────

class NoteCreate(BaseModel):
    content: Annotated[str, Field(min_length=5, description="Note content (at least 5 chars)")]
    author: Annotated[str, Field(min_length=2, description="Author name (at least 2 chars)")]


class NoteRead(NoteCreate):
    id: str


# ── Decisions ─────────────────────────────────────────────────────────────────

class DecisionCreate(BaseModel):
    summary: Annotated[str, Field(min_length=5, description="Decision summary (at least 5 chars)")]
    made_by: Annotated[str, Field(min_length=2, description="Person who made the decision")]


class DecisionRead(DecisionCreate):
    id: str


# ── Action Items ──────────────────────────────────────────────────────────────

class ActionItemStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"


class ActionItemCreate(BaseModel):
    description: Annotated[str, Field(min_length=3, description="Task description (at least 3 chars)")]
    owner: Annotated[str, Field(min_length=2, description="Responsible person (at least 2 chars)")]
    due_date: Annotated[date, Field(description="Due date (YYYY-MM-DD); must be today or in the future")]

    @model_validator(mode="after")
    def due_date_not_in_past(self) -> ActionItemCreate:
        if self.due_date < date.today():
            raise ValueError(f"due_date must be today or in the future, got {self.due_date}")
        return self


class ActionItemRead(ActionItemCreate):
    id: str
    status: ActionItemStatus = ActionItemStatus.open


class ActionItemStatusUpdate(BaseModel):
    status: ActionItemStatus


class ActionItemListResponse(BaseModel):
    total: int
    items: list[ActionItemRead]
