"""
Session 13 — API Testing: notes and decisions endpoints.

Demonstrates fixture chaining: created_note depends on created_meeting,
which depends on client — all wired automatically by pytest via conftest.py.
"""

from fastapi.testclient import TestClient


# ── Notes ─────────────────────────────────────────────────────────────────────

def test_create_note_returns_201(
    client: TestClient, created_meeting: dict, note_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(f"/meetings/{meeting_id}/notes", json=note_payload)
    assert r.status_code == 201
    body = r.json()
    assert body["content"] == note_payload["content"]
    assert body["author"] == note_payload["author"]
    assert "id" in body


def test_create_note_unknown_meeting_returns_404(
    client: TestClient, note_payload: dict
) -> None:
    r = client.post("/meetings/nonexistent/notes", json=note_payload)
    assert r.status_code == 404


def test_create_note_content_too_short_returns_422(
    client: TestClient, created_meeting: dict, note_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(
        f"/meetings/{meeting_id}/notes",
        json={**note_payload, "content": "Hi"},
    )
    assert r.status_code == 422


def test_list_notes_uses_fixture(
    client: TestClient, created_meeting: dict, created_note: dict
) -> None:
    """created_note fixture pre-populates data; just assert the list endpoint works."""
    meeting_id = created_meeting["id"]
    r = client.get(f"/meetings/{meeting_id}/notes")
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) == 1
    assert notes[0]["id"] == created_note["id"]


def test_list_notes_accumulates_multiple(
    client: TestClient, created_meeting: dict, note_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    client.post(f"/meetings/{meeting_id}/notes", json=note_payload)
    client.post(
        f"/meetings/{meeting_id}/notes",
        json={**note_payload, "content": "Second note content here"},
    )
    r = client.get(f"/meetings/{meeting_id}/notes")
    assert r.status_code == 200
    assert len(r.json()) == 2


# ── Decisions ─────────────────────────────────────────────────────────────────

def test_create_decision_returns_201(
    client: TestClient, created_meeting: dict, decision_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(f"/meetings/{meeting_id}/decisions", json=decision_payload)
    assert r.status_code == 201
    body = r.json()
    assert body["summary"] == decision_payload["summary"]
    assert body["made_by"] == decision_payload["made_by"]
    assert "id" in body


def test_create_decision_unknown_meeting_returns_404(
    client: TestClient, decision_payload: dict
) -> None:
    r = client.post("/meetings/nonexistent/decisions", json=decision_payload)
    assert r.status_code == 404


def test_create_decision_summary_too_short_returns_422(
    client: TestClient, created_meeting: dict, decision_payload: dict
) -> None:
    meeting_id = created_meeting["id"]
    r = client.post(
        f"/meetings/{meeting_id}/decisions",
        json={**decision_payload, "summary": "No"},
    )
    assert r.status_code == 422


def test_list_decisions_uses_fixture(
    client: TestClient, created_meeting: dict, created_decision: dict
) -> None:
    """created_decision fixture pre-populates data."""
    meeting_id = created_meeting["id"]
    r = client.get(f"/meetings/{meeting_id}/decisions")
    assert r.status_code == 200
    decisions = r.json()
    assert len(decisions) == 1
    assert decisions[0]["id"] == created_decision["id"]
