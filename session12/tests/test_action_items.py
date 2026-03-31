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


# ── POST /meetings/{id}/action-items ──────────────────────────────────────────

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


# ── Exercise: GET with owner filter ───────────────────────────────────────────

def test_list_action_items_returns_total_and_items(meeting_id):
    client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM)
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Review PR"})
    r = client.get(f"/meetings/{meeting_id}/action-items")
    assert r.status_code == 200
    body = r.json()
    assert "total" in body
    assert "items" in body
    assert body["total"] == 2
    assert len(body["items"]) == 2


def test_list_action_items_filter_by_owner(meeting_id):
    client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM)
    client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**VALID_ITEM, "description": "Deploy service", "owner": "Carol"},
    )
    r = client.get(f"/meetings/{meeting_id}/action-items?owner=Bob")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["owner"] == "Bob"


def test_list_action_items_filter_by_owner_no_match(meeting_id):
    client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM)
    r = client.get(f"/meetings/{meeting_id}/action-items?owner=Nonexistent")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_list_action_items_unknown_meeting_returns_404():
    r = client.get("/meetings/nonexistent/action-items")
    assert r.status_code == 404


# ── Challenge: pagination + stable ordering ───────────────────────────────────

def test_list_action_items_pagination_limit(meeting_id):
    for i in range(5):
        client.post(
            f"/meetings/{meeting_id}/action-items",
            json={**VALID_ITEM, "description": f"Task number {i + 1:02d}"},
        )
    r = client.get(f"/meetings/{meeting_id}/action-items?limit=3&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 3


def test_list_action_items_pagination_offset(meeting_id):
    for i in range(5):
        client.post(
            f"/meetings/{meeting_id}/action-items",
            json={**VALID_ITEM, "description": f"Task number {i + 1:02d}"},
        )
    r = client.get(f"/meetings/{meeting_id}/action-items?limit=3&offset=3")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2


def test_list_action_items_sorted_by_due_date(meeting_id):
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Later task 1", "due_date": "2026-08-01"})
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Earlier task", "due_date": "2026-05-01"})
    r = client.get(f"/meetings/{meeting_id}/action-items")
    body = r.json()
    dates = [item["due_date"] for item in body["items"]]
    assert dates == sorted(dates)


def test_list_action_items_limit_validation(meeting_id):
    r = client.get(f"/meetings/{meeting_id}/action-items?limit=0")
    assert r.status_code == 422


def test_list_action_items_limit_max_validation(meeting_id):
    r = client.get(f"/meetings/{meeting_id}/action-items?limit=101")
    assert r.status_code == 422


def test_list_action_items_offset_negative_validation(meeting_id):
    r = client.get(f"/meetings/{meeting_id}/action-items?offset=-1")
    assert r.status_code == 422


def test_list_action_items_filter_and_pagination_combined(meeting_id):
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Bob task A", "owner": "Bob", "due_date": "2026-05-01"})
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Bob task B", "owner": "Bob", "due_date": "2026-06-01"})
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Bob task C", "owner": "Bob", "due_date": "2026-07-01"})
    client.post(f"/meetings/{meeting_id}/action-items", json={**VALID_ITEM, "description": "Carol task", "owner": "Carol", "due_date": "2026-05-01"})
    r = client.get(f"/meetings/{meeting_id}/action-items?owner=Bob&limit=2&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2
    assert body["items"][0]["description"] == "Bob task A"
    assert body["items"][1]["description"] == "Bob task B"


# ── GET single + PATCH status ─────────────────────────────────────────────────

def test_get_action_item_returns_200(meeting_id):
    created = client.post(f"/meetings/{meeting_id}/action-items", json=VALID_ITEM).json()
    r = client.get(f"/meetings/{meeting_id}/action-items/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_action_item_not_found_returns_404(meeting_id):
    r = client.get(f"/meetings/{meeting_id}/action-items/999")
    assert r.status_code == 404


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
