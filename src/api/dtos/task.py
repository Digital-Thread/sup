from datetime import date, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.apps.task.domain import (
    AssignedId,
    FeatureId,
    OwnerId,
    Priority,
    Status,
    TagId,
    TaskId,
    WorkspaceId,
)
from src.apps.task.exceptions import TaskUpdateError
from src.apps.task import OrderByField, SortOrder


class SuccessResponse(BaseModel):
    message: str


class CreateTaskRequestDTO(BaseModel):
    workspace_id: WorkspaceId
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

    @field_validator('name', 'feature_id', 'assigned_to', 'priority', 'status', 'due_date')
    def fields_cannot_be_none(cls, value: Any, info: FieldValidationInfo) -> Any:
        if value is None:
            raise TaskUpdateError(
                message=f"Для поля '{info.field_name}' не может быть установлено значение None."
            )
        return value


class TaskResponseDTO(BaseModel):
    id: TaskId
    workspace_id: WorkspaceId
    name: str
    feature_id: FeatureId
    owner_id: OwnerId
    assigned_to: AssignedId
    due_date: date
    created_at: datetime
    updated_at: datetime
    description: str | None
    priority: Priority
    status: Status
    tags: list[TagId] | None
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
