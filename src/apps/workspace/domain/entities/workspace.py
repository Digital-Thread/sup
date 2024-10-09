from dataclasses import dataclass, field
from datetime import datetime, timezone
from re import match
from typing import Optional
from uuid import uuid4

from src.apps.workspace.domain.entities.validator_mixins import (
    DescriptionValidatorMixin,
)
from src.apps.workspace.domain.types_ids import (
    CategoryId,
    FeatureId,
    InviteId,
    MeetId,
    MemberId,
    OwnerId,
    ProjectId,
    RoleId,
    TagId,
    TaskId,
    WorkspaceId,
)


@dataclass
class Workspace(DescriptionValidatorMixin):
    owner_id: OwnerId
    _name: str
    _id: Optional[WorkspaceId] = field(default=None)
    _description: Optional[str] = field(default=None)
    logo: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    invite_ids: set[InviteId] = field(default_factory=set)
    project_ids: set[ProjectId] = field(default_factory=set)
    meet_ids: set[MeetId] = field(default_factory=set)
    tag_ids: set[TagId] = field(default_factory=set)
    role_ids: set[RoleId] = field(default_factory=set)
    member_ids: set[MemberId] = field(default_factory=set)
    member_roles: dict[MemberId, RoleId] = field(default_factory=dict)
    feature_tags: dict[FeatureId, set[TagId]] = field(default_factory=dict)
    task_tags: dict[TaskId, set[TagId]] = field(default_factory=dict)
    meet_categories: dict[MeetId, CategoryId] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name, 'рабочего пространства')

        if self._description:
            self._is_valid_description(self._description, 'рабочего пространства')

    @staticmethod
    def _is_valid_name(name: str, attr_name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s]{1,50}$'
        if not bool(match(pattern, name)):
            raise ValueError(f'Неверный формат названия {attr_name}')

    @property
    def id(self) -> WorkspaceId:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._is_valid_name(new_name, attr_name='рабочего пространства')
        self._name = new_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._is_valid_description(new_description, 'рабочего пространства')
        self._description = new_description
