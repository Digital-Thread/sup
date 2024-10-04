from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


class MeetRequest(BaseModel):
    name: str
    meet_at: datetime
    workspace_id: int
    category_id: int
    owner_id: int
    assigned_to: int


class MeetResponse(MeetRequest):
    id: int


class PaginatedResponse[M](GenericModel):
    count: int = Field(description='Number of items returned in the response')
    items: list[M] = Field(
        description='List of items returned in the response following given criteria'
    )
