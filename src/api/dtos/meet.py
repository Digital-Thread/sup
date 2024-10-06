from datetime import datetime
from typing import Literal

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


class CreateMeetResponse(BaseModel):
    id: int


class PaginatedParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: Literal[4, 8, 16, 24] = Field(16)

    @property
    def limit(self):
        return self.per_page

    @property
    def offset(self):
        return (self.page - 1) * self.per_page


class PaginatedResponse[M](GenericModel):
    count: int = Field(description='Number of items returned in the response')
    items: list[M] = Field(
        description='List of items returned in the response following given criteria'
    )
