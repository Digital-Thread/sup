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


class FeatureMember(TypedDict):
    id: UserId
    fullname: str
    avatar: str


class FeatureTag(TypedDict):
    id: TagId
    name: str
    color: str


@dataclass
class FeatureOutputDTO:
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


@dataclass
class FeatureInWorkspaceOutputDTO:
    id: FeatureId
    name: str
    project_name: str
    created_at: datetime
    priority: Priority
    status: Status
    members: list[FeatureMember] | None


class FeatureAttrsWithWorkspace(TypedDict):
    workspace_id: WorkspaceId
    project_id: ProjectId
    owner_id: OwnerId
    assigned_to: UserId
    tags: list[TagId]
    members: list[UserId]
