from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, Field

from src.apps.meet.dtos import MeetFilterFields, MeetResponseDTO, ParticipantResponseDTO


class SuccessResponse(BaseModel):
    message: str


class ParticipantRequest(BaseModel):
    user_id: UUID
    status: Literal['present', 'absent', 'warned']


class ParticipantRequestUpdate(BaseModel):
    status: Literal['present', 'absent', 'warned']


class ParticipantRequestDelete(BaseModel):
    id: int


class MeetRequestCreate(BaseModel):
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[ParticipantRequest]


class MeetRequestUpdate(BaseModel):
    name: str | None = None
    meet_at: datetime | None = None
    category_id: int | None = None
    assigned_to: UUID | None = None
    participants_to_add: list[ParticipantRequest] = Field(default_factory=list)
    participants_to_update: list[ParticipantRequestUpdate] = Field(default_factory=list)
    participants_to_delete: list[ParticipantRequestDelete] = Field(default_factory=list)


class ParticipantResponse(BaseModel):
    id: int
    user_id: UUID
    status: Literal['present', 'absent', 'warned']

    @staticmethod
    def from_dto(dto: ParticipantResponseDTO) -> 'ParticipantResponse':
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
    def from_dto(dto: MeetResponseDTO) -> 'MeetResponse':
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
    def limit(self) -> Literal[4, 8, 16, 24] | None:
        return self.per_page

    @property
    def offset(self) -> int:
        if self.per_page is None:
            return 0
        return (self.page - 1) * self.per_page


class MeetFilterFieldsRequest(BaseModel):
    category_id: int | None = None
    assigned_to: UUID | None = None
    meet_at: datetime | None = None

    def to_dto(self) -> MeetFilterFields:
        result: MeetFilterFields = {}

        if self.category_id is not None:
            result['category_id'] = self.category_id
        if self.assigned_to is not None:
            result['assigned_to'] = self.assigned_to
        if self.meet_at is not None:
            result['meet_at'] = self.meet_at
        return result


class MeetSortFieldsRequest(BaseModel):
    field: Literal['meet_at', 'name', 'assigned_to'] = 'meet_at'
    order: Literal['ASC', 'DESC'] = 'DESC'


class PaginatedResponse[M](BaseModel):
    count: int = Field(description='Number of items returned in the response')
    items: list[M] = Field(
        description='List of items returned in the response following given criteria'
    )
