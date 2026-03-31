"""
Session 14 — Tutorial: OpenAPI metadata and error documentation.

Verifies that the app exposes correct OpenAPI metadata and that
error responses are documented in the spec.
"""

from fastapi.testclient import TestClient


# ── OpenAPI info metadata ─────────────────────────────────────────────────────

def test_openapi_info_title(client: TestClient) -> None:
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert r.json()["info"]["title"] == "Meeting Note Assistant API"


def test_openapi_info_version(client: TestClient) -> None:
    r = client.get("/openapi.json")
    assert r.json()["info"]["version"] == "0.2.0"


def test_openapi_info_description_present(client: TestClient) -> None:
    r = client.get("/openapi.json")
    description = r.json()["info"]["description"]
    assert description and len(description) > 10


def test_openapi_tags_declared(client: TestClient) -> None:
    """All domain tags must appear in the top-level tags list."""
    r = client.get("/openapi.json")
    tag_names = {t["name"] for t in r.json().get("tags", [])}
    assert {"meetings", "notes", "decisions", "action-items", "dashboard"}.issubset(tag_names)


# ── Error responses documented in spec ───────────────────────────────────────

def test_get_meeting_404_documented(client: TestClient) -> None:
    """GET /meetings/{id} must document a 404 response."""
    r = client.get("/openapi.json")
    spec = r.json()
    responses = spec["paths"]["/meetings/{meeting_id}"]["get"]["responses"]
    assert "404" in responses


def test_post_meeting_422_documented(client: TestClient) -> None:
    """POST /meetings must document a 422 response."""
    r = client.get("/openapi.json")
    spec = r.json()
    responses = spec["paths"]["/meetings"]["post"]["responses"]
    assert "422" in responses


def test_patch_meeting_status_404_and_422_documented(client: TestClient) -> None:
    """PATCH /meetings/{id}/status must document both 404 and 422."""
    r = client.get("/openapi.json")
    spec = r.json()
    responses = spec["paths"]["/meetings/{meeting_id}/status"]["patch"]["responses"]
    assert "404" in responses
    assert "422" in responses


def test_dashboard_summary_in_spec(client: TestClient) -> None:
    """GET /dashboard/summary must be present in the spec."""
    r = client.get("/openapi.json")
    assert "/dashboard/summary" in r.json()["paths"]


# ── Docs UI reachable ─────────────────────────────────────────────────────────

def test_swagger_ui_reachable(client: TestClient) -> None:
    r = client.get("/docs")
    assert r.status_code == 200


def test_redoc_reachable(client: TestClient) -> None:
    r = client.get("/redoc")
    assert r.status_code == 200
