from fastapi import FastAPI

from api.routers.meetings import router as meetings_router
from api.routers.notes import router as notes_router
from api.routers.decisions import router as decisions_router
from api.routers.action_items import router as action_items_router

app = FastAPI(title="Meeting Note Assistant — Session 13")

app.include_router(meetings_router)
app.include_router(notes_router)
app.include_router(decisions_router)
app.include_router(action_items_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
