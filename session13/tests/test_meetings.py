"""
Session 13 — API Testing: meetings endpoint.

Tutorial : test_health_ok, test_create_meeting_ok
Exercise : 3 tests for POST /meetings (1 success + 2 validation errors)
"""

from fastapi.testclient import TestClient


# ── Tutorial ──────────────────────────────────────────────────────────────────

def test_health_ok(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_meeting_ok(client: TestClient, meeting_payload: dict) -> None:
    r = client.post("/meetings", json=meeting_payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == meeting_payload["title"]
    assert body["owner"] == meeting_payload["owner"]
    assert body["status"] == "scheduled"
    assert "id" in body


# ── Exercise: POST /meetings — 1 success + 2 errors ──────────────────────────

def test_create_meeting_returns_201_with_all_fields(
    client: TestClient, meeting_payload: dict
) -> None:
    """Success: response contains every field from the payload plus id/status."""
    r = client.post("/meetings", json=meeting_payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == meeting_payload["title"]
    assert body["date"] == meeting_payload["date"]
    assert body["owner"] == meeting_payload["owner"]
    assert body["participants"] == meeting_payload["participants"]
    assert body["status"] == "scheduled"
    assert "id" in body


def test_create_meeting_missing_required_field_returns_422(client: TestClient) -> None:
    """Error 1: omitting a required field (owner) must return 422 Unprocessable Entity."""
    r = client.post(
        "/meetings",
        json={"title": "Planning", "date": "2026-04-01", "participants": ["Bob"]},
    )
    assert r.status_code == 422


def test_create_meeting_title_too_short_returns_422(
    client: TestClient, meeting_payload: dict
) -> None:
    """Error 2: title shorter than 3 characters violates the min_length constraint."""
    r = client.post("/meetings", json={**meeting_payload, "title": "AB"})
    assert r.status_code == 422


# ── GET /meetings ─────────────────────────────────────────────────────────────

def test_list_meetings_empty_returns_zero_total(client: TestClient) -> None:
    r = client.get("/meetings")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_list_meetings_returns_total_and_items(
    client: TestClient, meeting_payload: dict
) -> None:
    client.post("/meetings", json=meeting_payload)
    client.post("/meetings", json={**meeting_payload, "title": "Retro Meeting"})
    r = client.get("/meetings")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


def test_list_meetings_filter_by_owner(client: TestClient, meeting_payload: dict) -> None:
    client.post("/meetings", json=meeting_payload)
    client.post("/meetings", json={**meeting_payload, "title": "Retro", "owner": "Jorge"})
    r = client.get("/meetings?owner=Alice")
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["owner"] == "Alice"


def test_list_meetings_pagination_limit(
    client: TestClient, meeting_payload: dict
) -> None:
    for i in range(5):
        client.post("/meetings", json={**meeting_payload, "title": f"Meeting {i + 1:02d}"})
    r = client.get("/meetings?limit=3&offset=0")
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 3


def test_list_meetings_sorted_by_date(
    client: TestClient, meeting_payload: dict
) -> None:
    client.post("/meetings", json={**meeting_payload, "title": "Later", "date": "2026-06-01"})
    client.post("/meetings", json={**meeting_payload, "title": "Earlier", "date": "2026-04-01"})
    r = client.get("/meetings")
    dates = [item["date"] for item in r.json()["items"]]
    assert dates == sorted(dates)


# ── GET /meetings/{id} ────────────────────────────────────────────────────────

def test_get_meeting_returns_200(client: TestClient, created_meeting: dict) -> None:
    r = client.get(f"/meetings/{created_meeting['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created_meeting["id"]


def test_get_meeting_not_found_returns_404(client: TestClient) -> None:
    r = client.get("/meetings/nonexistent-id")
    assert r.status_code == 404


# ── PUT /meetings/{id} ────────────────────────────────────────────────────────

def test_put_meeting_updates_title(
    client: TestClient, created_meeting: dict, meeting_payload: dict
) -> None:
    r = client.put(
        f"/meetings/{created_meeting['id']}",
        json={**meeting_payload, "title": "Updated Title"},
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Updated Title"


def test_put_meeting_not_found_returns_404(
    client: TestClient, meeting_payload: dict
) -> None:
    r = client.put("/meetings/nonexistent-id", json=meeting_payload)
    assert r.status_code == 404


# ── PATCH /meetings/{id}/status ───────────────────────────────────────────────

def test_patch_status_scheduled_to_in_progress(
    client: TestClient, created_meeting: dict
) -> None:
    r = client.patch(
        f"/meetings/{created_meeting['id']}/status", json={"status": "in_progress"}
    )
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"


def test_patch_status_invalid_transition_returns_422(
    client: TestClient, created_meeting: dict
) -> None:
    # scheduled → completed is not a valid transition
    r = client.patch(
        f"/meetings/{created_meeting['id']}/status", json={"status": "completed"}
    )
    assert r.status_code == 422


def test_patch_status_terminal_state_returns_422(
    client: TestClient, created_meeting: dict
) -> None:
    client.patch(
        f"/meetings/{created_meeting['id']}/status", json={"status": "cancelled"}
    )
    r = client.patch(
        f"/meetings/{created_meeting['id']}/status", json={"status": "scheduled"}
    )
    assert r.status_code == 422


# ── DELETE /meetings/{id} ─────────────────────────────────────────────────────

def test_delete_meeting_returns_204(
    client: TestClient, created_meeting: dict
) -> None:
    r = client.delete(f"/meetings/{created_meeting['id']}")
    assert r.status_code == 204
    assert client.get(f"/meetings/{created_meeting['id']}").status_code == 404


def test_delete_meeting_not_found_returns_404(client: TestClient) -> None:
    r = client.delete("/meetings/nonexistent-id")
    assert r.status_code == 404
