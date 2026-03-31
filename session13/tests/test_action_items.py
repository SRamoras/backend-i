"""
Session 13 — API Testing: action items endpoint.

All fixtures (client, created_meeting, action_item_payload, etc.)
come from conftest.py — no setup boilerplate needed here.
"""

from fastapi.testclient import TestClient


# ── POST /meetings/{id}/action-items ─────────────────────────────────────────

def test_create_action_item_returns_201(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(f"/meetings/{meeting_id}/action-items", json=action_item_payload)
    assert r.status_code == 201
    body = r.json()
    assert body["description"] == action_item_payload["description"]
    assert body["owner"] == action_item_payload["owner"]
    assert body["status"] == "open"
    assert "id" in body


def test_create_action_item_unknown_meeting_returns_404(
    client: TestClient, action_item_payload: dict
) -> None:
    r = client.post("/meetings/nonexistent/action-items", json=action_item_payload)
    assert r.status_code == 404


def test_create_action_item_description_too_short_returns_422(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**action_item_payload, "description": "AB"},
    )
    assert r.status_code == 422


def test_create_action_item_past_due_date_returns_422(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**action_item_payload, "due_date": "2020-01-01"},
    )
    assert r.status_code == 422


def test_create_action_item_invalid_date_format_returns_422(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**action_item_payload, "due_date": "not-a-date"},
    )
    assert r.status_code == 422


# ── GET /meetings/{id}/action-items ──────────────────────────────────────────

def test_list_action_items_uses_fixture(
    client: TestClient, created_action_item: dict, created_meeting: dict
) -> None:
    """created_action_item fixture sets up data; we just verify the GET response."""
    meeting_id = created_meeting["id"]
    r = client.get(f"/meetings/{meeting_id}/action-items")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == created_action_item["id"]


def test_list_action_items_filter_by_owner(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    client.post(f"/meetings/{meeting_id}/action-items", json=action_item_payload)
    client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**action_item_payload, "description": "Deploy service", "owner": "Carol"},
    )
    r = client.get(f"/meetings/{meeting_id}/action-items?owner=Bob")
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["owner"] == "Bob"


def test_list_action_items_sorted_by_due_date(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**action_item_payload, "description": "Later task", "due_date": "2026-08-01"},
    )
    client.post(
        f"/meetings/{meeting_id}/action-items",
        json={**action_item_payload, "description": "Earlier task", "due_date": "2026-05-01"},
    )
    r = client.get(f"/meetings/{meeting_id}/action-items")
    dates = [item["due_date"] for item in r.json()["items"]]
    assert dates == sorted(dates)


def test_list_action_items_pagination(
    client: TestClient, created_meeting: dict, action_item_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    for i in range(5):
        client.post(
            f"/meetings/{meeting_id}/action-items",
            json={**action_item_payload, "description": f"Task number {i + 1:02d}"},
        )
    r = client.get(f"/meetings/{meeting_id}/action-items?limit=3&offset=0")
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 3


# ── GET single action item ────────────────────────────────────────────────────

def test_get_action_item_returns_200(
    client: TestClient, created_meeting: dict, created_action_item: dict
) -> None:
    meeting_id = created_meeting["id"]
    item_id = created_action_item["id"]
    r = client.get(f"/meetings/{meeting_id}/action-items/{item_id}")
    assert r.status_code == 200
    assert r.json()["id"] == item_id


def test_get_action_item_not_found_returns_404(
    client: TestClient, created_meeting: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.get(f"/meetings/{meeting_id}/action-items/999")
    assert r.status_code == 404


# ── PATCH status ──────────────────────────────────────────────────────────────

def test_patch_action_item_status_to_in_progress(
    client: TestClient, created_meeting: dict, created_action_item: dict
) -> None:
    meeting_id = created_meeting["id"]
    item_id = created_action_item["id"]
    r = client.patch(
        f"/meetings/{meeting_id}/action-items/{item_id}/status",
        json={"status": "in_progress"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"


def test_patch_action_item_status_to_completed(
    client: TestClient, created_meeting: dict, created_action_item: dict
) -> None:
    meeting_id = created_meeting["id"]
    item_id = created_action_item["id"]
    r = client.patch(
        f"/meetings/{meeting_id}/action-items/{item_id}/status",
        json={"status": "completed"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
