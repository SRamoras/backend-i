import pytest
from fastapi.testclient import TestClient
from api.main import api
from api.routers.meetings import DB

client = TestClient(api)

VALID_PAYLOAD = {
    "title": "Sprint Planning",
    "date": "2026-04-01",
    "owner": "Alice",
    "participants": ["Bob", "Carol"],
}


@pytest.fixture(autouse=True)
def clear_db():
    DB.clear()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_meeting_returns_201():
    r = client.post("/meetings", json=VALID_PAYLOAD)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == VALID_PAYLOAD["title"]
    assert body["status"] == "scheduled"
    assert "id" in body


def test_create_meeting_missing_field_returns_422():
    r = client.post("/meetings", json={"title": "No owner"})
    assert r.status_code == 422


def test_create_meeting_title_too_short_returns_422():
    r = client.post("/meetings", json={**VALID_PAYLOAD, "title": "AB"})
    assert r.status_code == 422


def test_create_meeting_empty_participants_returns_422():
    r = client.post("/meetings", json={**VALID_PAYLOAD, "participants": []})
    assert r.status_code == 422


def test_get_meeting_returns_200():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    r = client.get(f"/meetings/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_meeting_not_found_returns_404():
    r = client.get("/meetings/nonexistent")
    assert r.status_code == 404


# ── Tutorial: list with pagination ────────────────────────────────────────────

def test_list_meetings_returns_total_and_items():
    client.post("/meetings", json=VALID_PAYLOAD)
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Retro Meeting"})
    r = client.get("/meetings")
    assert r.status_code == 200
    body = r.json()
    assert "total" in body
    assert "items" in body
    assert body["total"] == 2
    assert len(body["items"]) == 2


def test_list_meetings_filter_by_owner():
    client.post("/meetings", json=VALID_PAYLOAD)
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Retro Meeting", "owner": "Jorge"})
    r = client.get("/meetings?owner=Alice")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["owner"] == "Alice"


def test_list_meetings_filter_by_owner_no_match():
    client.post("/meetings", json=VALID_PAYLOAD)
    r = client.get("/meetings?owner=Nonexistent")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_list_meetings_pagination_limit():
    for i in range(5):
        client.post("/meetings", json={**VALID_PAYLOAD, "title": f"Meeting {i + 1:02d}"})
    r = client.get("/meetings?limit=3&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 3


def test_list_meetings_pagination_offset():
    for i in range(5):
        client.post("/meetings", json={**VALID_PAYLOAD, "title": f"Meeting {i + 1:02d}"})
    r = client.get("/meetings?limit=3&offset=3")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2


def test_list_meetings_sorted_by_date():
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Later Meeting", "date": "2026-06-01"})
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Earlier Meeting", "date": "2026-04-01"})
    r = client.get("/meetings")
    body = r.json()
    dates = [item["date"] for item in body["items"]]
    assert dates == sorted(dates)


def test_list_meetings_limit_validation():
    r = client.get("/meetings?limit=0")
    assert r.status_code == 422


def test_list_meetings_limit_max_validation():
    r = client.get("/meetings?limit=101")
    assert r.status_code == 422


def test_list_meetings_offset_negative_validation():
    r = client.get("/meetings?offset=-1")
    assert r.status_code == 422


def test_list_meetings_filter_and_pagination_combined():
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Alice A", "owner": "Alice", "date": "2026-04-01"})
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Alice B", "owner": "Alice", "date": "2026-05-01"})
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Alice C", "owner": "Alice", "date": "2026-06-01"})
    client.post("/meetings", json={**VALID_PAYLOAD, "title": "Jorge A", "owner": "Jorge", "date": "2026-04-01"})
    r = client.get("/meetings?owner=Alice&limit=2&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2
    assert body["items"][0]["title"] == "Alice A"
    assert body["items"][1]["title"] == "Alice B"


# ── Existing CRUD tests ───────────────────────────────────────────────────────

def test_put_meeting_updates_fields():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    r = client.put(f"/meetings/{created['id']}", json={**VALID_PAYLOAD, "title": "Updated Title"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated Title"


def test_put_meeting_preserves_status():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    client.patch(f"/meetings/{created['id']}/status", json={"status": "in_progress"})
    r = client.put(f"/meetings/{created['id']}", json=VALID_PAYLOAD)
    assert r.json()["status"] == "in_progress"


def test_put_meeting_not_found_returns_404():
    r = client.put("/meetings/nonexistent", json=VALID_PAYLOAD)
    assert r.status_code == 404


def test_patch_status_scheduled_to_in_progress():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    r = client.patch(f"/meetings/{created['id']}/status", json={"status": "in_progress"})
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"


def test_patch_status_invalid_transition_returns_422():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    r = client.patch(f"/meetings/{created['id']}/status", json={"status": "completed"})
    assert r.status_code == 422


def test_patch_status_terminal_state_returns_422():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    client.patch(f"/meetings/{created['id']}/status", json={"status": "cancelled"})
    r = client.patch(f"/meetings/{created['id']}/status", json={"status": "scheduled"})
    assert r.status_code == 422


def test_delete_meeting_returns_204():
    created = client.post("/meetings", json=VALID_PAYLOAD).json()
    r = client.delete(f"/meetings/{created['id']}")
    assert r.status_code == 204
    assert client.get(f"/meetings/{created['id']}").status_code == 404


def test_delete_meeting_not_found_returns_404():
    r = client.delete("/meetings/nonexistent")
    assert r.status_code == 404
