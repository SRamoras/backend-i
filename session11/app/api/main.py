from fastapi import FastAPI

from api.routers.meetings import router as meetings_router
from api.routers.notes import router as notes_router
from api.routers.decisions import router as decisions_router
from api.routers.action_items import router as action_items_router

api = FastAPI(title="Meeting Note Assistant — Session 11")

api.include_router(meetings_router)
api.include_router(notes_router)
api.include_router(decisions_router)
api.include_router(action_items_router)


@api.get("/health")
def health() -> dict:
    return {"status": "ok"}
