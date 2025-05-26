from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from src.apps.meet import FilterField, OrderByField, SortOrder
from src.apps.meet.domain import (
    AssignedId,
    CategoryId,
    MeetId,
    OwnerId,
    ParticipantId,
    WorkspaceId,
)


class CreateMeetRequestDTO(BaseModel):
    name: str
    meet_at: datetime
    owner_id: OwnerId
    category_id: CategoryId | None = None
    assigned_to: AssignedId | None = None
    participants: list[ParticipantId] | None = None


class UpdateMeetRequestDTO(BaseModel):
    name: str | None = None
    meet_at: datetime | None = None
    category_id: CategoryId | None = None
    assigned_to: AssignedId | None = None
    participants: list[ParticipantId] | None = None


class MeetResponseDTO(BaseModel):
    id: MeetId
    workspace_id: WorkspaceId
    name: str
    meet_at: datetime
    category_id: CategoryId | None
    owner_id: OwnerId
    assigned_to: AssignedId | None
    participants: list[ParticipantId] | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )


class PageLimits(StrEnum):
    ALL = 'all'
    FOUR = '4'
    EIGHT = '8'
    SIXTEEN = '16'
    TWENTYFOUR = '24'

    @property
    def limit_by(self) -> Literal[4, 8, 16, 24, None]:
        limits: dict[PageLimits, Literal[4, 8, 16, 24, None]] = {
            PageLimits.ALL: None,
            PageLimits.FOUR: 4,
            PageLimits.EIGHT: 8,
            PageLimits.SIXTEEN: 16,
            PageLimits.TWENTYFOUR: 24,
        }
        return limits[self]


class QueryParams(BaseModel):
    filter_by_name: str | None = None
    filter_by_category: CategoryId | None = None
    filter_by_assigned_to: AssignedId | None = None
    filter_by_meet_at: datetime | None = None
    order_by_field: OrderByField = OrderByField.MEET_AT
    sort_order: SortOrder = SortOrder.DESC

    page: int = Field(1, ge=1)
    per_page: PageLimits = PageLimits.SIXTEEN

    @property
    def offset(self) -> int:
        if self.per_page.limit_by is None:
            return 0
        return (self.page - 1) * self.per_page.limit_by

    @property
    def filters(self) -> FilterField | None:
        filter = FilterField()
        if self.filter_by_name is not None:
            filter['name'] = self.filter_by_name
        if self.filter_by_category is not None:
            filter['category'] = self.filter_by_category
        if self.filter_by_assigned_to is not None:
            filter['assigned_to'] = self.filter_by_assigned_to
        if self.filter_by_meet_at is not None:
            filter['meet_at'] = self.filter_by_meet_at

        return filter if filter else None
