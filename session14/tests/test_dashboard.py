"""
Session 14 — Challenge: GET /dashboard/summary aggregate endpoint.
"""

from fastapi.testclient import TestClient


def test_dashboard_summary_empty(client: TestClient) -> None:
    """Empty state: all counters are zero."""
    r = client.get("/dashboard/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["total_meetings"] == 0
    assert body["total_action_items"] == 0
    assert body["total_notes"] == 0
    assert body["total_decisions"] == 0


def test_dashboard_summary_counts_meetings(
    client: TestClient, meeting_payload: dict
) -> None:
    client.post("/meetings", json=meeting_payload)
    client.post("/meetings", json={**meeting_payload, "title": "Retro Meeting"})
    r = client.get("/dashboard/summary")
    assert r.json()["total_meetings"] == 2


def test_dashboard_summary_meetings_by_status(
    client: TestClient, meeting_payload: dict
) -> None:
    """After creating 1 meeting and advancing it, status counts must reflect reality."""
    resp = client.post("/meetings", json=meeting_payload)
    meeting_id = resp.json()["id"]
    client.patch(f"/meetings/{meeting_id}/status", json={"status": "in_progress"})

    body = client.get("/dashboard/summary").json()
    assert body["meetings_by_status"]["scheduled"] == 0
    assert body["meetings_by_status"]["in_progress"] == 1


def test_dashboard_summary_counts_action_items(
    client: TestClient,
    created_meeting: dict,
    action_item_payload: dict,
) -> None:
    mid = created_meeting["id"]
    client.post(f"/meetings/{mid}/action-items", json=action_item_payload)
    client.post(
        f"/meetings/{mid}/action-items",
        json={**action_item_payload, "description": "Deploy service"},
    )
    body = client.get("/dashboard/summary").json()
    assert body["total_action_items"] == 2


def test_dashboard_summary_action_items_by_status(
    client: TestClient,
    created_meeting: dict,
    created_action_item: dict,
) -> None:
    mid = created_meeting["id"]
    item_id = created_action_item["id"]
    client.patch(
        f"/meetings/{mid}/action-items/{item_id}/status",
        json={"status": "completed"},
    )
    body = client.get("/dashboard/summary").json()
    assert body["action_items_by_status"]["completed"] == 1
    assert body["action_items_by_status"]["open"] == 0


def test_dashboard_summary_counts_notes(
    client: TestClient,
    created_meeting: dict,
    note_payload: dict,
) -> None:
    mid = created_meeting["id"]
    client.post(f"/meetings/{mid}/notes", json=note_payload)
    client.post(f"/meetings/{mid}/notes", json={**note_payload, "content": "Second note here"})
    body = client.get("/dashboard/summary").json()
    assert body["total_notes"] == 2


def test_dashboard_summary_counts_decisions(
    client: TestClient,
    created_meeting: dict,
    decision_payload: dict,
) -> None:
    mid = created_meeting["id"]
    client.post(f"/meetings/{mid}/decisions", json=decision_payload)
    body = client.get("/dashboard/summary").json()
    assert body["total_decisions"] == 1


def test_dashboard_summary_aggregates_across_meetings(
    client: TestClient,
    meeting_payload: dict,
    note_payload: dict,
    action_item_payload: dict,
) -> None:
    """Metrics must aggregate across multiple meetings, not just the last one."""
    r1 = client.post("/meetings", json=meeting_payload)
    r2 = client.post("/meetings", json={**meeting_payload, "title": "Retro"})
    mid1, mid2 = r1.json()["id"], r2.json()["id"]

    client.post(f"/meetings/{mid1}/notes", json=note_payload)
    client.post(f"/meetings/{mid2}/notes", json=note_payload)
    client.post(f"/meetings/{mid1}/action-items", json=action_item_payload)

    body = client.get("/dashboard/summary").json()
    assert body["total_meetings"] == 2
    assert body["total_notes"] == 2
    assert body["total_action_items"] == 1


def test_dashboard_summary_schema_fields(client: TestClient) -> None:
    """Response must contain all required top-level fields."""
    body = client.get("/dashboard/summary").json()
    required = {
        "total_meetings",
        "meetings_by_status",
        "total_action_items",
        "action_items_by_status",
        "total_notes",
        "total_decisions",
    }
    assert required.issubset(body.keys())
