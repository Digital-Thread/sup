from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict

from src.apps.feature.domain import (
    FeatureId,
    OptionalFeatureUpdateFields,
    OwnerId,
    Priority,
    ProjectId,
    Status,
    TagId,
    UserId,
    WorkspaceId,
    TaskId,
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
    tasks: list[TaskId] | None = None


class FeatureMember(TypedDict):
    id: UserId
    fullname: str
    avatar: str


@dataclass
class FeaturesInWorkspaceOutputDTO:
    id: FeatureId
    name: str
    project_name: str
    created_at: datetime
    priority: Priority
    status: Status
    members: list[FeatureMember] | None
