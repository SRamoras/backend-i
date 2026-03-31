from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import date
from typing import Annotated, Any


# ── Request / Response schemas ────────────────────────────────────────────────

class MeetingCreate(BaseModel):
    """Payload required to create a meeting."""

    title: Annotated[str, Field(min_length=3, description="Meeting title (at least 3 characters)")]
    date: Annotated[date, Field(description="Meeting date in ISO-8601 format (YYYY-MM-DD)")]
    owner: Annotated[str, Field(min_length=2, description="Owner name (at least 2 characters)")]
    participants: Annotated[
        list[str],
        Field(min_length=1, description="Non-empty list of participant names"),
    ]


class MeetingRead(MeetingCreate):
    """Full meeting representation returned by the API."""

    id: Annotated[str, Field(description="Unique meeting identifier (UUID)")]


# ── Standard error schemas (Challenge) ───────────────────────────────────────

class ErrorDetail(BaseModel):
    """A single validation or error detail entry."""

    loc: list[Any]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    """Standard error envelope returned for all 4xx responses."""

    status_code: int
    detail: str
    errors: list[ErrorDetail] = []
