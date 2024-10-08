from datetime import datetime, timezone
from enum import IntEnum
from re import match
from typing import TypedDict

from apps.feature.domain.aliases import OwnerId, ProjectId, TagId, UserId, WorkspaceId


class Priority(IntEnum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NO_PRIORITY = 1

    @property
    def display(self) -> str:
        return {
            5: 'Критическая',
            4: 'Высокая',
            3: 'Средняя',
            2: 'Низкая',
            1: 'Не задана',
        }[self.value]


class Status(IntEnum):
    FINISH = 4
    TEST = 3
    DEVELOPMENT = 2
    NEW = 1

    @property
    def display(self) -> str:
        return {
            4: 'Готово',
            3: 'Тестирование',
            2: 'Разработка',
            1: 'Новая',
        }[self.value]


class OptionalFeatureUpdateFields(TypedDict, total=False):
    name: str
    project_id: ProjectId
    assigned_to: UserId | None
    description: str | None
    priority: Priority
    status: Status
    tags: set[TagId] | None
    members: set[UserId] | None


class Feature:

    def __init__(
        self,
        name: str,
        workspace_id: WorkspaceId,
        project_id: ProjectId,
        owner_id: OwnerId,
        assigned_to: UserId | None = None,
        description: str | None = None,
        priority: Priority = Priority.NO_PRIORITY,
        status: Status = Status.NEW,
        tags: set[TagId] | None = None,
        members: set[UserId] | None = None,
    ):
        self.name = name
        self._workspace_id = workspace_id
        self.project_id = project_id
        self._owner_id = owner_id
        self.assigned_to = assigned_to
        self.description = description
        self.priority = priority
        self.status = status
        self.tags = tags if tags else set()
        self.members = members if members else set()
        self._created_at = datetime.now(timezone.utc)
        self._updated_at = datetime.now(timezone.utc)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._validate_name(value)
        self._name = value

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        self._validate_description(value)
        self._description = value

    def _validate_name(self, name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ ]+$'
        max_length = 50
        if not match(pattern, name):
            raise ValueError(
                'В названии допускается использование только букв латинского и кириллического алфавитов.'
            )
        if len(name) > max_length:
            raise ValueError(f'В названии может быть максимум {max_length} символов.')

    def _validate_description(self, description: str | None) -> None:
        max_length = 10_000
        if description is not None and len(description) > max_length:
            raise ValueError(f'В описании может быть максимум {max_length} символов.')

    @property
    def workspace_id(self) -> WorkspaceId:
        return self._workspace_id

    @property
    def owner_id(self) -> OwnerId:
        return self._owner_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def mark_as_updated(self) -> None:
        self._updated_at = datetime.now(timezone.utc)

    def update_fields(self, updates: OptionalFeatureUpdateFields) -> None:
        for field, value in updates.items():
            setattr(self, field, value)
        self.mark_as_updated()
