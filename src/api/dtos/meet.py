from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, Field

from src.apps.meet.dtos import MeetResponseDTO, ParticipantResponseDTO


class ParticipantRequest(BaseModel):
    user_id: UUID
    status: str


class MeetRequest(BaseModel):
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[ParticipantRequest]


class ParticipantResponse(BaseModel):
    id: int
    user_id: UUID
    status: str

    @staticmethod
    def from_dto(dto: ParticipantResponseDTO):
        return ParticipantResponse(id=dto.id, user_id=dto.user_id, status=dto.status)


class MeetResponse(BaseModel):
    id: int
    name: str
    meet_at: datetime
    category_id: int
    owner_id: UUID
    assigned_to: UUID
    participants: list[ParticipantResponse]

    @staticmethod
    def from_dto(dto: MeetResponseDTO):
        return MeetResponse(
            id=dto.id,
            name=dto.name,
            meet_at=dto.meet_at,
            category_id=dto.category_id,
            owner_id=dto.owner_id,
            assigned_to=dto.assigned_to,
            participants=[ParticipantResponse.from_dto(p) for p in dto.participants],
        )


class CreateMeetResponse(BaseModel):
    id: int


class PaginatedParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: Annotated[Literal[4, 8, 16, 24] | None, BeforeValidator(int)] = 16

    @property
    def limit(self):
        return self.per_page

    @property
    def offset(self):
        if self.per_page is None:
            return 0
        return (self.page - 1) * self.per_page


class MeetFilterFieldsRequest(BaseModel):
    category_id: int | None = None
    assigned_to: UUID | None = None
    meet_at: datetime | None = None


class MeetSortFieldsRequest(BaseModel):
    field: Literal['meet_at', 'name', 'assigned_to'] = 'meet_at'
    order: Literal['ASC', 'DESC'] = 'DESC'


class PaginatedResponse[M](BaseModel):
    count: int = Field(description='Number of items returned in the response')
    items: list[M] = Field(
        description='List of items returned in the response following given criteria'
    )
