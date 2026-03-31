import pytest
from fastapi.testclient import TestClient
from api.main import api
from api.routers.meetings import DB as MEETINGS_DB
from api.routers.action_items import ACTION_DB

client = TestClient(api)

MEETING_PAYLOAD = {
    "title": "Sprint Planning",
    "date": "2026-04-01",
    "owner": "Alice",
    "participants": ["Bob", "Carol"],
}

VALID_ITEM = {
    "description": "Write unit tests",
    "owner": "Bob",
    "due_date": "2026-05-01",
}


@pytest.fixture(autouse=True)
def clear_dbs():
    MEETINGS_DB.clear()
    ACTION_DB.clear()


@pytest.fixture()
def meeting_id() -> str:
    return client.post("/meetings", json=MEETING_PAYLOAD).json()["id"]


# ── Tutorial: POST /meetings/{id}/action-items ─────────────────────────────────

def test_create_action_item_returns_201(meeting_id):
    r = client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM)
    assert r.status_code == 201
    body = r.json()
    assert body["description"] == VALID_ITEM["description"]
    assert body["owner"] == VALID_ITEM["owner"]
    assert body["due_date"] == VALID_ITEM["due_date"]
    assert body["status"] == "open"
    assert "id" in body


def test_create_action_item_unknown_meeting_returns_404():
    r = client.post("/meetings/nonexistent/action-items", json=VALID_ITEM)
    assert r.status_code == 404


def test_create_action_item_description_too_short_returns_422(meeting_id):
    r = client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "AB"})
    assert r.status_code == 422


def test_create_action_item_owner_too_short_returns_422(meeting_id):
    r = client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "owner": "X"})
    assert r.status_code == 422


# ── Challenge: due_date must be today or in the future ─────────────────────────

def test_create_action_item_past_due_date_returns_422(meeting_id):
    r = client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**VALID_ITEM, "due_date": "2020-01-01"},
    )
    assert r.status_code == 422


def test_create_action_item_invalid_date_format_returns_422(meeting_id):
    r = client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**VALID_ITEM, "due_date": "not-a-date"},
    )
    assert r.status_code == 422


# ── Exercise: GET /meetings/{id}/action-items ──────────────────────────────────

def test_list_action_items_returns_all(meeting_id):
    client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM)
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Review PR"})
    r = client.get(f"/meetings/{meeting_id}/action-items")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_list_action_items_unknown_meeting_returns_404():
    r = client.get("/meetings/nonexistent/action-items")
    assert r.status_code == 404


def test_get_action_item_returns_200(meeting_id):
    created = client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM).json()
    r = client.get(f"/meetings/{meeting_id}/action-items/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_action_item_not_found_returns_404(meeting_id):
    r = client.get(f"/meetings/{meeting_id}/action-items/999")
    assert r.status_code == 404


# ── Challenge: PATCH status ────────────────────────────────────────────────────

def test_patch_action_item_status_to_in_progress(meeting_id):
    created = client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM).json()
    r = client.patch(
        f"/meetings/{meeting_id}/action-items/{created['id']}/status",
        json={"status": "in_progress"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"


def test_patch_action_item_status_to_completed(meeting_id):
    created = client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM).json()
    r = client.patch(
        f"/meetings/{meeting_id}/action-items/{created['id']}/status",
        json={"status": "completed"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "completed"


def test_patch_action_item_status_not_found_returns_404(meeting_id):
    r = client.patch(
        f"/meetings/{meeting_id}/action-items/999/status",
        json={"status": "completed"},
    )
    assert r.status_code == 404
