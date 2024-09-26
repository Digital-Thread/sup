from dataclasses import dataclass, field
from typing import TypedDict

from apps.feature.domain.entities.feature import Priority, Status
from apps.feature.domain.value_objects import (
    FeatureId,
    OwnerId,
    ProjectId,
    TagId,
    UserId,
)


@dataclass
class FeatureInputDTO:
    name: str
    project_id: ProjectId
    owner_id: OwnerId
    assigned_to: UserId | None = None
    description: str | None = None
    priority: Priority = Priority.NO_PRIORITY
    status: Status = Status.NEW
    tags: set[TagId] | None = None
    members: set[UserId] | None = None


class OptionalFeatureUpdateFields(TypedDict, total=False):
    name: str
    project_id: ProjectId
    assigned_to: UserId | None
    description: str | None
    priority: Priority
    status: Status
    tags: set[TagId] | None
    members: set[UserId] | None


@dataclass
class FeatureUpdateDTO:
    id: FeatureId
    updated_fields: OptionalFeatureUpdateFields
