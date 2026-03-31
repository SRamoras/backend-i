from fastapi import FastAPI

from api.routers.meetings import router as meetings_router

api = FastAPI(title="Meetings CRUD API — Session 10")

api.include_router(meetings_router)


@api.get("/health")
def health() -> dict:
    return {"status": "ok"}
