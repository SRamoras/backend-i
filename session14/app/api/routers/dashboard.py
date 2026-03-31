from fastapi import APIRouter

from api.schemas import (
    ActionItemStatusCounts,
    DashboardSummary,
    MeetingStatusCounts,
)
from api.routers.meetings import DB as MEETINGS_DB
from api.routers.action_items import ACTION_DB
from api.routers.notes import NOTES_DB
from api.routers.decisions import DECISIONS_DB

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummary,
    summary="Aggregate metrics across all meetings",
)
def get_dashboard_summary() -> DashboardSummary:
    meetings = list(MEETINGS_DB.values())

    meetings_by_status = MeetingStatusCounts(
        scheduled=sum(1 for m in meetings if m.status.value == "scheduled"),
        in_progress=sum(1 for m in meetings if m.status.value == "in_progress"),
        completed=sum(1 for m in meetings if m.status.value == "completed"),
        cancelled=sum(1 for m in meetings if m.status.value == "cancelled"),
    )

    all_items = [item for items in ACTION_DB.values() for item in items]
    action_items_by_status = ActionItemStatusCounts(
        open=sum(1 for i in all_items if i.status.value == "open"),
        in_progress=sum(1 for i in all_items if i.status.value == "in_progress"),
        completed=sum(1 for i in all_items if i.status.value == "completed"),
    )

    total_notes = sum(len(notes) for notes in NOTES_DB.values())
    total_decisions = sum(len(decisions) for decisions in DECISIONS_DB.values())

    return DashboardSummary(
        total_meetings=len(meetings),
        meetings_by_status=meetings_by_status,
        total_action_items=len(all_items),
        action_items_by_status=action_items_by_status,
        total_notes=total_notes,
        total_decisions=total_decisions,
    )
