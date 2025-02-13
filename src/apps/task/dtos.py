from dataclasses import dataclass
from datetime import date, datetime
from typing import Self

from src.apps.task.domain import (
    AssignedId,
    FeatureId,
    OptionalTaskUpdateFields,
    OwnerId,
    Priority,
    Status,
    TagId,
    TaskEntity,
    TaskId,
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


@dataclass
class TaskOutputDTO:
    id: TaskId
    workspace_id: WorkspaceId
    name: str
    feature_id: FeatureId
    owner_id: OwnerId
    assigned_to: AssignedId
    due_date: date
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: list[TagId] | None = None

    @classmethod
    def from_entity(cls, task_id: TaskId, entity: TaskEntity) -> Self:
        return cls(
            id=task_id,
            workspace_id=entity.workspace_id,
            name=entity.name,
            feature_id=entity.feature_id,
            owner_id=entity.owner_id,
            assigned_to=entity.assigned_to,
            due_date=entity.due_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            description=entity.description,
            priority=entity.priority,
            status=entity.status,
            tags=entity.tags,
        )
