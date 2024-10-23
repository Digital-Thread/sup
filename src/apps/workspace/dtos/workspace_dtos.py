from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict
from uuid import UUID


class CreateWorkspaceAppDTO(TypedDict):
    name: str
    owner_id: UUID


@dataclass
class WorkspaceAppDTO:
    id: UUID
    owner_id: UUID
    name: str
    created_at: datetime
    description: str | None = field(default=None)
    logo: str | None = field(default=None)
    invite_ids: list[int] = field(default_factory=list)
    project_ids: list[int] = field(default_factory=list)
    meet_ids: list[int] = field(default_factory=list)
    tag_ids: list[int] = field(default_factory=list)
    role_ids: list[int] = field(default_factory=list)
    member_ids: list[UUID] = field(default_factory=list)
    member_roles: dict[UUID, int] = field(default_factory=dict)
    feature_tags: dict[int, set[int]] = field(default_factory=dict)
    task_tags: dict[int, set[int]] = field(default_factory=dict)
    meet_categories: dict[int, int] = field(default_factory=dict)


class UpdateWorkspaceAppDTO(TypedDict, total=False):
    name: str
    description: str
    logo: str
