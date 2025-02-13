from datetime import date, datetime, timezone
from enum import StrEnum
from re import match
from typing import TypedDict

from src.apps.task.domain.types_ids import (
    AssignedId,
    FeatureId,
    OwnerId,
    TagId,
    WorkspaceId,
)


class Priority(StrEnum):
    CRITICAL = 'Критическая'
    HIGH = 'Высокая'
    MEDIUM = 'Средняя'
    LOW = 'Низкая'
    NO_PRIORITY = 'Не задана'


class Status(StrEnum):
    FINISH = 'Готово'
    BACKLOG = 'Бэклог'
    TEST = 'Тестирование'
    DEVELOPMENT = 'Разработка'
    NEW = 'Новая'


class OptionalTaskUpdateFields(TypedDict, total=False):
    name: str
    feature_id: FeatureId
    assigned_to: AssignedId
    description: str | None
    priority: Priority
    status: Status
    due_date: date
    tags: list[TagId] | None


class TaskEntity:

    def __init__(
            self,
            name: str,
            workspace_id: WorkspaceId,
            feature_id: FeatureId,
            owner_id: OwnerId,
            assigned_to: AssignedId,
            due_date: date,
            description: str | None = None,
            priority: Priority = Priority.NO_PRIORITY,
            status: Status = Status.NEW,
            tags: list[TagId] | None = None,
    ):
        self.name = name
        self._workspace_id = workspace_id
        self.feature_id = feature_id
        self._owner_id = owner_id
        self.assigned_to = assigned_to
        self.due_date = due_date
        self.description = description
        self.priority = priority
        self.status = status
        self.tags = tags
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

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

    def update_fields(self, updates: OptionalTaskUpdateFields) -> None:
        for field, value in updates.items():
            setattr(self, field, value)
        self.updated_at = datetime.now(timezone.utc)
