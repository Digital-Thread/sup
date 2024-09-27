from datetime import datetime

from pydantic import BaseModel


class MeetRequest(BaseModel):
    name: str
    meet_at: datetime
    workspace_id: int
    category_id: int
    owner_id: int
    assigned_to: int


class MeetResponse(MeetRequest):
    id: int
