from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from re import match
from typing import Any
from uuid import uuid4

from apps.feature.domain.value_objects import (
    FeatureId,
    OwnerId,
    ProjectId,
    TagId,
    UserId,
)


class Priority(IntEnum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NO_PRIORITY = 1

    @property
    def display(self) -> str:
        return {
            5: "Критическая",
            4: "Высокая",
            3: "Средняя",
            2: "Низкая",
            1: "Не задана",
        }[self.value]


class Status(IntEnum):
    FINISH = 4
    TEST = 3
    DEVELOPMENT = 2
    NEW = 1

    @property
    def display(self) -> str:
        return {
            4: "Готово",
            3: "Тестирование",
            2: "Разработка",
            1: "Новая",
        }[self.value]


@dataclass
class Feature:
    _name: str
    project_id: ProjectId
    _owner_id: OwnerId
    assigned_to: UserId | None = field(default=None)
    _description: str | None = field(default=None)
    priority: Priority = field(default=Priority.NO_PRIORITY)
    status: Status = field(default=Status.NEW)
    tags: set[TagId] = field(default_factory=set)
    members: set[UserId] = field(default_factory=set)
    _id: FeatureId = field(default_factory=uuid4, init=False)
    _created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc), init=False
    )
    _updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc), init=False
    )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._validate_name(value)
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._validate_description(value)
        self._description = value

    def _validate_name(self, name: str) -> None:
        pattern = r"^[a-zA-Zа-яА-ЯёЁ]+$"
        max_length = 50
        if not match(pattern, name):
            raise ValueError(
                "В названии допускается использование только букв латинского и кириллического алфавитов."
            )
        if len(name) > max_length:
            raise ValueError(
                f"В названии может быть максимум {max_length} символов."
            )

    def _validate_description(self, description: str | None) -> None:
        max_length = 10_000
        if description is not None and len(description) > max_length:
            raise ValueError(
                f"В описании может быть максимум {max_length} символов."
            )

    @property
    def owner_id(self) -> OwnerId:
        return self._owner_id

    @property
    def id(self) -> FeatureId:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def __setattr__(self, key: str, value: Any) -> None:
        if key != "updated_at" and hasattr(self, "_updated_at"):
            super().__setattr__("_updated_at", datetime.now(timezone.utc))
        super().__setattr__(key, value)
