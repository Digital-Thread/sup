from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, TypedDict
from uuid import UUID

from src.apps.workspace.dtos.base_dto import BaseDTO


class CreateWorkspaceAppDTO(TypedDict):
    name: str
    owner_id: UUID


@dataclass
class WorkspaceAppDTO(BaseDTO):
    id: UUID
    owner_id: UUID
    name: str
    created_at: datetime
    description: Optional[str] = field(default=None)
    logo: Optional[str] = field(default=None)
    invite_ids: set[int] = field(default_factory=set)
    project_ids: set[int] = field(default_factory=set)
    meet_ids: set[int] = field(default_factory=set)
    tag_ids: set[int] = field(default_factory=set)
    role_ids: set[int] = field(default_factory=set)
    member_ids: set[UUID] = field(default_factory=set)
    member_roles: dict[UUID, int] = field(default_factory=dict)
    feature_tags: dict[int, set[int]] = field(default_factory=dict)
    task_tags: dict[int, set[int]] = field(default_factory=dict)
    meet_categories: dict[int, int] = field(default_factory=dict)


class UpdateWorkspaceAppDTO(TypedDict, total=False):
    name: str
    description: str
    logo: str
    invite_ids: set[int]
    project_ids: set[int]
    meet_ids: set[int]
    tag_ids: set[int]
    role_ids: set[int]
    member_ids: set[UUID]
    member_roles: dict[UUID, int]
    feature_tags: dict[int, set[int]]
    task_tags: dict[int, set[int]]
    meet_categories: dict[int, int]
