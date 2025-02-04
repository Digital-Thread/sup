from datetime import datetime, timezone
from enum import StrEnum
from re import match
from typing import TypedDict

from src.apps.feature.domain.types_ids import (
    OwnerId,
    ProjectId,
    TagId,
    UserId,
    WorkspaceId,
    FeatureId,
    TaskId,
)


class Priority(StrEnum):
    CRITICAL = 'Критическая'
    HIGH = 'Высокая'
    MEDIUM = 'Средняя'
    LOW = 'Низкая'
    NO_PRIORITY = 'Не задана'


class Status(StrEnum):
    FINISH = 'Готово'
    TEST = 'Тестирование'
    DEVELOPMENT = 'Разработка'
    NEW = 'Новая'


class OptionalFeatureUpdateFields(TypedDict, total=False):
    name: str
    project_id: ProjectId
    assigned_to: UserId | None
    description: str | None
    priority: Priority
    status: Status
    tags: list[TagId] | None
    members: list[UserId] | None


class FeatureEntity:

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
            tags: list[TagId] | None = None,
            members: list[UserId] | None = None,
            tasks: list[TaskId] | None = None,
    ):
        self._id: FeatureId | None = None
        self.name = name
        self._workspace_id = workspace_id
        self.project_id = project_id
        self._owner_id = owner_id
        self.assigned_to = assigned_to
        self.description = description
        self.priority = priority
        self.status = status
        self.tags = tags
        self.members = members
        self.tasks = tasks
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id: FeatureId):
        if self._id is not None:
            raise AttributeError('Идентификатор фичи уже установлен')

        self._id = _id

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

    def update_fields(self, updates: OptionalFeatureUpdateFields) -> None:
        for field, value in updates.items():
            setattr(self, field, value)
        self.updated_at = datetime.now(timezone.utc)
