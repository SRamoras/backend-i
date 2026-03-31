from fastapi import FastAPI

from api.routers.meetings import router as meetings_router
from api.routers.notes import router as notes_router
from api.routers.decisions import router as decisions_router
from api.routers.action_items import router as action_items_router
from api.routers.dashboard import router as dashboard_router

# ── Tutorial: OpenAPI metadata ────────────────────────────────────────────────

app = FastAPI(
    title="Meeting Note Assistant API",
    version="0.2.0",
    description=(
        "Meetings, notes, and action items management.\n\n"
        "## Features\n"
        "- Full CRUD for meetings with status machine\n"
        "- Notes and decisions per meeting\n"
        "- Action items with owner and due date tracking\n"
        "- Dashboard summary with aggregate metrics\n\n"
        "## Error handling\n"
        "All errors return `{\"detail\": \"<message>\"}` with the appropriate HTTP status code."
    ),
    contact={
        "name": "Backend I Course",
        "url": "https://github.com/backend-i",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {"name": "meetings", "description": "Meeting lifecycle: create, list, update, delete, and transition status."},
        {"name": "notes", "description": "Notes attached to a specific meeting."},
        {"name": "decisions", "description": "Decisions recorded during a meeting."},
        {"name": "action-items", "description": "Action items assigned to participants."},
        {"name": "dashboard", "description": "Aggregate metrics across all meetings."},
    ],
)

app.include_router(meetings_router)
app.include_router(notes_router)
app.include_router(decisions_router)
app.include_router(action_items_router)
app.include_router(dashboard_router)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict:
    return {"status": "ok"}
