from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from src.apps.feature import (
    FeatureMember,
    FeatureTag,
    FilterField,
    OrderByField,
    SortOrder,
)
from src.apps.feature.domain import (
    FeatureId,
    OwnerId,
    Priority,
    ProjectId,
    Status,
    TagId,
    UserId,
)


class CreateFeatureRequestDTO(BaseModel):
    name: str
    project_id: ProjectId
    owner_id: OwnerId
    assigned_to: UserId | None = None
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: list[TagId] | None = None
    members: list[UserId] | None = None


class UpdateFeatureRequestDTO(BaseModel):
    name: str | None = None
    project_id: ProjectId | None = None
    assigned_to: UserId | None = None
    description: str | None = None
    priority: Priority | None = None
    status: Status | None = None
    tags: list[TagId] | None = None
    members: list[UserId] | None = None


class FeatureResponseDTO(BaseModel):
    id: FeatureId
    name: str
    project_name: str
    owner: FeatureMember
    created_at: datetime
    updated_at: datetime
    assigned_to: FeatureMember | None
    description: str | None
    priority: Priority
    status: Status
    tags: list[FeatureTag] | None
    members: list[FeatureMember] | None
    model_config = ConfigDict(
        from_attributes=True,
    )


class FeaturesResponseDTO(BaseModel):
    id: FeatureId
    name: str
    project_name: str
    created_at: datetime
    priority: Priority
    status: Status
    members: list[FeatureMember] | None
    model_config = ConfigDict(
        from_attributes=True,
    )


class PageLimits(StrEnum):
    ALL = 'all'
    FIVE = '5'
    TEN = '10'

    @property
    def limit_by(self) -> Literal[5, 10, None]:
        if self == self.ALL:
            return None
        elif self == self.FIVE:
            return 5
        elif self == self.TEN:
            return 10

        return None


class QueryParams(BaseModel):
    filter_by_members: list[UserId] | None = None
    filter_by_tags: list[TagId] | None = None
    filter_by_statuses: list[Status] | None = None
    filter_by_projects: list[ProjectId] | None = None

    order_by_field: OrderByField = OrderByField.PRIORITY
    sort_order: SortOrder = SortOrder.DESC

    page: int = Field(1, ge=1)
    per_page: PageLimits = PageLimits.TEN

    @property
    def offset(self) -> int:
        if self.per_page.limit_by is None:
            return 0
        return (self.page - 1) * self.per_page.limit_by

    @property
    def filters(self) -> FilterField | None:
        filter = FilterField()
        if self.filter_by_members is not None:
            filter['members'] = self.filter_by_members
        if self.filter_by_tags is not None:
            filter['tags'] = self.filter_by_tags
        if self.filter_by_statuses is not None:
            filter['status'] = self.filter_by_statuses
        if self.filter_by_projects is not None:
            filter['project'] = self.filter_by_projects

        return filter if filter else None
