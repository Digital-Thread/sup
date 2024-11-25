from dataclasses import dataclass
from datetime import datetime
from typing import Self

from src.apps.feature.domain import (
    FeatureEntity,
    FeatureId,
    OptionalFeatureUpdateFields,
    OwnerId,
    Priority,
    ProjectId,
    Status,
    TagId,
    UserId,
    WorkspaceId,
)


@dataclass
class FeatureInputDTO:
    workspace_id: WorkspaceId
    name: str
    project_id: ProjectId
    owner_id: OwnerId
    assigned_to: UserId | None = None
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: list[TagId] | None = None
    members: list[UserId] | None = None


@dataclass
class FeatureUpdateDTO:
    id: FeatureId
    updated_fields: OptionalFeatureUpdateFields


@dataclass
class FeatureOutputDTO:
    id: FeatureId
    workspace_id: WorkspaceId
    name: str
    project_id: ProjectId
    owner_id: OwnerId
    created_at: datetime
    updated_at: datetime
    assigned_to: UserId | None = None
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: list[TagId] | None = None
    members: list[UserId] | None = None

    @classmethod
    def from_entity(cls, feature_id: FeatureId, entity: FeatureEntity) -> Self:
        return cls(
            id=feature_id,
            workspace_id=entity.workspace_id,
            name=entity.name,
            project_id=entity.project_id,
            owner_id=entity.owner_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            assigned_to=entity.assigned_to,
            description=entity.description,
            priority=entity.priority,
            status=entity.status,
            tags=entity.tags,
            members=entity.members,
        )
