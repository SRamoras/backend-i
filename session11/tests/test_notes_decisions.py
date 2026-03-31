import pytest
from fastapi.testclient import TestClient
from api.main import api
from api.routers.meetings import DB as MEETINGS_DB
from api.routers.notes import NOTES_DB
from api.routers.decisions import DECISIONS_DB

client = TestClient(api)

MEETING_PAYLOAD = {
    "title": "Sprint Planning",
    "date": "2026-04-01",
    "owner": "Alice",
    "participants": ["Bob", "Carol"],
}


@pytest.fixture(autouse=True)
def clear_dbs():
    MEETINGS_DB.clear()
    NOTES_DB.clear()
    DECISIONS_DB.clear()


@pytest.fixture()
def meeting_id() -> str:
    return client.post("/meetings", json=MEETING_PAYLOAD).json()["id"]


# ── Notes ──────────────────────────────────────────────────────────────────────

def test_create_note_returns_201(meeting_id):
    r = client.post(
        f"/meetings/{meeting_id}/notes",
        json={"content": "Team discussed rollout plan", "author": "Alice"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["content"] == "Team discussed rollout plan"
    assert "id" in body


def test_create_note_unknown_meeting_returns_404():
    r = client.post(
        "/meetings/nonexistent/notes",
        json={"content": "Some note here", "author": "Bob"},
    )
    assert r.status_code == 404


def test_create_note_content_too_short_returns_422(meeting_id):
    r = client.post(
        f"/meetings/{meeting_id}/notes",
        json={"content": "Hi", "author": "Alice"},
    )
    assert r.status_code == 422


def test_list_notes(meeting_id):
    client.post(f"/meetings/{meeting_id}/notes", json={"content": "First note text", "author": "Alice"})
    client.post(f"/meetings/{meeting_id}/notes", json={"content": "Second note text", "author": "Bob"})
    r = client.get(f"/meetings/{meeting_id}/notes")
    assert r.status_code == 200
    assert len(r.json()) == 2


# ── Decisions ──────────────────────────────────────────────────────────────────

def test_create_decision_returns_201(meeting_id):
    r = client.post(
        f"/meetings/{meeting_id}/decisions",
        json={"summary": "Adopt trunk-based development", "made_by": "Alice"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["summary"] == "Adopt trunk-based development"
    assert "id" in body


def test_create_decision_unknown_meeting_returns_404():
    r = client.post(
        "/meetings/nonexistent/decisions",
        json={"summary": "Some decision here", "made_by": "Bob"},
    )
    assert r.status_code == 404


def test_create_decision_summary_too_short_returns_422(meeting_id):
    r = client.post(
        f"/meetings/{meeting_id}/decisions",
        json={"summary": "No", "made_by": "Alice"},
    )
    assert r.status_code == 422


def test_list_decisions(meeting_id):
    client.post(
        f"/meetings/{meeting_id}/decisions",
        json={"summary": "Use PostgreSQL for storage", "made_by": "Alice"},
    )
    client.post(
        f"/meetings/{meeting_id}/decisions",
        json={"summary": "Ship feature behind flag", "made_by": "Bob"},
    )
    r = client.get(f"/meetings/{meeting_id}/decisions")
    assert r.status_code == 200
    assert len(r.json()) == 2
