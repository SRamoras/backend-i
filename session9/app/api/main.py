from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from uuid import uuid4

from app.api.schemas import MeetingCreate, MeetingRead, ErrorResponse, ErrorDetail

api = FastAPI(title="Meeting Note Assistant API — Session 9")

# In-memory store: { id: MeetingRead }
_store: dict[str, MeetingRead] = {}


# ── Custom exception handlers (Challenge) ────────────────────────────────────

@api.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return a standard ErrorResponse envelope for 422 Unprocessable Entity."""
    errors = [
        ErrorDetail(
            loc=[str(part) for part in err["loc"]],
            msg=err["msg"],
            type=err["type"],
        )
        for err in exc.errors()
    ]
    body = ErrorResponse(
        status_code=422,
        detail="Validation failed",
        errors=errors,
    )
    return JSONResponse(status_code=422, content=body.model_dump())


@api.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Return a standard ErrorResponse envelope for all HTTP errors."""
    body = ErrorResponse(
        status_code=exc.status_code,
        detail=str(exc.detail),
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


# ── Endpoints ─────────────────────────────────────────────────────────────────

@api.get("/health")
def health() -> dict:
    return {"status": "ok"}


@api.post("/meetings", response_model=MeetingRead, status_code=201)
def create_meeting(payload: MeetingCreate) -> MeetingRead:
    meeting = MeetingRead(id=str(uuid4()), **payload.model_dump())
    _store[meeting.id] = meeting
    return meeting


@api.get("/meetings", response_model=list[MeetingRead])
def list_meetings() -> list[MeetingRead]:
    return list(_store.values())


@api.get("/meetings/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: str) -> MeetingRead:
    meeting = _store.get(meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@api.delete("/meetings/{meeting_id}", status_code=204)
def delete_meeting(meeting_id: str) -> None:
    if meeting_id not in _store:
        raise HTTPException(status_code=404, detail="Meeting not found")
    del _store[meeting_id]


# ── Dev entrypoint ────────────────────────────────────────────────────────────

def start() -> None:
    import uvicorn
    uvicorn.run("app.api.main:api", host="0.0.0.0", port=8000, reload=True)
