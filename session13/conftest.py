"""
Challenge: reusable fixtures for meetings and action items data.

Fixtures defined here are available to every test file automatically.
pytest discovers conftest.py at collection time and injects fixtures by name.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent / "app"))

from api.main import app
from api.routers.meetings import DB as MEETINGS_DB
from api.routers.action_items import ACTION_DB
from api.routers.notes import NOTES_DB
from api.routers.decisions import DECISIONS_DB


# ── Infrastructure ────────────────────────────────────────────────────────────

@pytest.fixture()
def client() -> TestClient:
    """Shared HTTP test client — one per test."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_dbs() -> None:
    """Reset all in-memory stores before every test so tests are independent."""
    MEETINGS_DB.clear()
    ACTION_DB.clear()
    NOTES_DB.clear()
    DECISIONS_DB.clear()


# ── Meeting fixtures ──────────────────────────────────────────────────────────

@pytest.fixture()
def meeting_payload() -> dict:
    """Valid meeting creation payload."""
    return {
        "title": "Sprint Planning",
        "date": "2026-04-01",
        "owner": "Alice",
        "participants": ["Bob", "Carol"],
    }


@pytest.fixture()
def created_meeting(client: TestClient, meeting_payload: dict) -> dict:
    """A meeting that already exists in the database."""
    r = client.post("/meetings", json=meeting_payload)
    assert r.status_code == 201
    return r.json()


# ── Action item fixtures ──────────────────────────────────────────────────────

@pytest.fixture()
def action_item_payload() -> dict:
    """Valid action item creation payload."""
    return {
        "description": "Write unit tests",
        "owner": "Bob",
        "due_date": "2026-05-01",
    }


@pytest.fixture()
def created_action_item(
    client: TestClient,
    created_meeting: dict,
    action_item_payload: dict,
) -> dict:
    """An action item that already exists under the created_meeting."""
    meeting_id = created_meeting["id"]
    r = client.post(f"/meetings/{meeting_id}/action-items", json=action_item_payload)
    assert r.status_code == 201
    return r.json()


# ── Note fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture()
def note_payload() -> dict:
    """Valid note creation payload."""
    return {"content": "Discussed Q2 roadmap in detail", "author": "Carol"}


@pytest.fixture()
def created_note(client: TestClient, created_meeting: dict, note_payload: dict) -> dict:
    """A note that already exists under the created_meeting."""
    meeting_id = created_meeting["id"]
    r = client.post(f"/meetings/{meeting_id}/notes", json=note_payload)
    assert r.status_code == 201
    return r.json()


# ── Decision fixtures ─────────────────────────────────────────────────────────

@pytest.fixture()
def decision_payload() -> dict:
    """Valid decision creation payload."""
    return {"summary": "Adopt trunk-based development", "made_by": "Alice"}


@pytest.fixture()
def created_decision(
    client: TestClient, created_meeting: dict, decision_payload: dict
) -> dict:
    """A decision that already exists under the created_meeting."""
    meeting_id = created_meeting["id"]
    r = client.post(f"/meetings/{meeting_id}/decisions", json=decision_payload)
    assert r.status_code == 201
    return r.json()
