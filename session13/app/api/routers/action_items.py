from fastapi import APIRouter, HTTPException, Query, status

from api.schemas import (
    ActionItemCreate,
    ActionItemListResponse,
    ActionItemRead,
    ActionItemStatus,
    ActionItemStatusUpdate,
)
from api.routers.meetings import DB as MEETINGS_DB

router = APIRouter(prefix="/meetings", tags=["action-items"])

ACTION_DB: dict[str, list[ActionItemRead]] = {}


def _require_meeting(meeting_id: str) -> None:
    if meeting_id not in MEETINGS_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")


def _require_item(meeting_id: str, item_id: str) -> ActionItemRead:
    items = ACTION_DB.get(meeting_id, [])
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found")


@router.post(
    "/{meeting_id}/action-items",
    response_model=ActionItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_action_item(meeting_id: str, payload: ActionItemCreate) -> ActionItemRead:
    _require_meeting(meeting_id)
    items = ACTION_DB.setdefault(meeting_id, [])
    item = ActionItemRead(id=str(len(items) + 1), **payload.model_dump())
    items.append(item)
    return item


@router.get("/{meeting_id}/action-items", response_model=ActionItemListResponse)
def list_action_items(
    meeting_id: str,
    owner: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ActionItemListResponse:
    _require_meeting(meeting_id)
    items = list(ACTION_DB.get(meeting_id, []))
    if owner:
        items = [i for i in items if i.owner == owner]
    items = sorted(items, key=lambda i: (i.due_date, i.id))
    total = len(items)
    return ActionItemListResponse(total=total, items=items[offset: offset + limit])


@router.get("/{meeting_id}/action-items/{item_id}", response_model=ActionItemRead)
def get_action_item(meeting_id: str, item_id: str) -> ActionItemRead:
    _require_meeting(meeting_id)
    return _require_item(meeting_id, item_id)


@router.patch("/{meeting_id}/action-items/{item_id}/status", response_model=ActionItemRead)
def update_action_item_status(
    meeting_id: str, item_id: str, payload: ActionItemStatusUpdate
) -> ActionItemRead:
    _require_meeting(meeting_id)
    item = _require_item(meeting_id, item_id)

    if payload.status == ActionItemStatus.completed:
        if not item.owner or len(item.owner) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Cannot complete an action item without a valid owner.",
            )
        if item.due_date is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Cannot complete an action item without a valid due date.",
            )

    item.status = payload.status
    return item
