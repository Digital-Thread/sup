from dataclasses import dataclass, field
from datetime import datetime, timezone
from re import match

from src.apps.workspace.domain.entities.validator_mixins import (
    DescriptionValidatorMixin,
)
from src.apps.workspace.domain.types_ids import (
    InviteId,
    MeetId,
    MemberId,
    OwnerId,
    ProjectId,
    RoleId,
    TagId,
    WorkspaceId,
)


@dataclass
class Workspace(DescriptionValidatorMixin):
    owner_id: OwnerId
    _name: str
    _id: WorkspaceId | None = field(default=None)
    _description: str | None = field(default=None)
    logo: str | None = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    invite_ids: list[InviteId] = field(default_factory=list)
    project_ids: list[ProjectId] = field(default_factory=list)
    meet_ids: list[MeetId] = field(default_factory=list)
    tag_ids: list[TagId] = field(default_factory=list)
    role_ids: list[RoleId] = field(default_factory=list)
    member_ids: list[MemberId] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name)

        if self._description:
            self._is_valid_description(self._description, 'рабочего пространства')

    @staticmethod
    def _is_valid_name(name: str) -> None:
        if not name.strip():
            raise ValueError('Имя рабочего пространства должно содержать хотя бы одну букву')

        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s]{1,50}$'
        if not bool(match(pattern, name)):
            raise ValueError(f'Неверный формат названия рабочего пространства')

    @property
    def id(self) -> WorkspaceId | None:
        return self._id

    @id.setter
    def id(self, new_id: WorkspaceId) -> None:
        if self._id is not None:
            raise AttributeError('Идентификатор рабочего пространства уже установлен')

        self._id = new_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._is_valid_name(new_name)
        self._name = new_name

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._is_valid_description(new_description, 'рабочего пространства')
        self._description = new_description
