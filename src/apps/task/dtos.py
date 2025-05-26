from dataclasses import dataclass
from datetime import date, datetime
from typing import TypedDict

from src.apps.task.domain import (
    AssignedId,
    FeatureId,
    OptionalTaskUpdateFields,
    OwnerId,
    Priority,
    Status,
    TagId,
    TaskId,
    UserId,
    WorkspaceId,
)


@dataclass
class TaskInputDTO:
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


@dataclass
class TaskUpdateDTO:
    id: TaskId
    updated_fields: OptionalTaskUpdateFields


class TaskMember(TypedDict):
    id: UserId
    fullname: str
    avatar: str


class FeatureInfo(TypedDict):
    id: FeatureId
    name: str


class TaskTag(TypedDict):
    id: TagId
    name: str
    color: str


@dataclass
class TaskOutputDTO:
    id: TaskId
    name: str
    owner: TaskMember
    feature: FeatureInfo
    feature_lead: TaskMember
    assigned_to: TaskMember
    created_at: datetime
    updated_at: datetime
    due_date: date
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: list[TaskTag] | None = None


@dataclass
class TaskInFeatureOutputDTO:
    id: TaskId
    name: str
    assigned_to: TaskMember
    created_at: datetime
    due_date: date
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW


class TaskAttrsWithWorkspace(TypedDict):
    workspace_id: WorkspaceId
    feature_id: FeatureId
    owner_id: OwnerId
    assigned_to: AssignedId
    tags: list[TagId]
