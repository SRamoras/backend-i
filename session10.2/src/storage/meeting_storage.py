from ..models.meeting_model import Meeting
from uuid import UUID

meeting_storage: dict[UUID, Meeting] = {}
