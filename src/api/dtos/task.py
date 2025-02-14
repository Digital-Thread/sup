from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from src.apps.task.domain import (
    AssignedId,
    FeatureId,
    OwnerId,
    Priority,
    Status,
    TagId,
    TaskId,
)
from src.apps.task import (
    OrderByField,
    SortOrder,
    TaskMember,
    TaskTag,
    FeatureInfo,
)


class CreateTaskRequestDTO(BaseModel):
    name: str
    feature_id: FeatureId
    owner_id: OwnerId
    assigned_to: AssignedId
    due_date: date
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: list[TagId] | None = None


class UpdateTaskRequestDTO(BaseModel):
    name: str | None = None
    feature_id: FeatureId | None = None
    assigned_to: AssignedId | None = None
    description: str | None = None
    priority: Priority | None = None
    status: Status | None = None
    due_date: date | None = None
    tags: list[TagId] | None = None


class TaskResponseDTO(BaseModel):
    id: TaskId
    name: str
    owner: TaskMember
    feature: FeatureInfo
    feature_lead: TaskMember
    assigned_to: TaskMember
    created_at: datetime
    updated_at: datetime
    due_date: date
    description: str | None
    priority: Priority
    status: Status
    tags: list[TaskTag] | None
    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskForFeatureResponseDTO(BaseModel):
    id: TaskId
    name: str
    assigned_to: TaskMember
    created_at: datetime
    due_date: date
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
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
    feature_id: FeatureId

    order_by_field: OrderByField = OrderByField.PRIORITY
    sort_order: SortOrder = SortOrder.DESC

    page: int = Field(1, ge=1)
    per_page: PageLimits = PageLimits.TEN

    @property
    def offset(self) -> int:
        if self.per_page.limit_by is None:
            return 0
        return (self.page - 1) * self.per_page.limit_by
