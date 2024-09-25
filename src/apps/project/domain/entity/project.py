from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from re import match
from typing import Optional, Set
from uuid import UUID


class StatusProject(Enum):
    DISCUSSION = 'В обсуждении'
    DEVELOPMENT = 'В разработке'
    SUPPORT = 'В поддержке'
    PAUSE = 'На паузе'
    CLOSED = 'Закрыт'


@dataclass
class Project:
    _name: str
    workspace_id: UUID
    owner_id: UUID
    id: Optional[int] = field(default=None)
    logo: Optional[str] = field(default=None)
    _description: Optional[str] = field(default=None)
    _status: StatusProject = field(default=StatusProject.DISCUSSION)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_to: Set[UUID] = field(default_factory=set)

    def __post_init__(self) -> None:
        self._validate_name(self._name)

        if self._description is not None:
            self._validate_description(self._description)

    @staticmethod
    def _validate_name(name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s]{1,20}$'
        if not bool(match(pattern, name)):
            raise ValueError(
                'Название проекта должно содержать только буквы русского и латинского алфавита.'
                'Длина не должна превышать 20 символов.'
            )

    @staticmethod
    def _validate_description(description: Optional[str]) -> None:
        if not len(description) <= 500:
            raise ValueError('Длина описания не должна превышать 500 символов.')

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._validate_name(new_name)
        self._name = new_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._validate_description(new_description)
        self._description = new_description

    @property
    def status(self) -> StatusProject:
        return self._status

    @status.setter
    def status(self, new_status: StatusProject) -> None:
        if not isinstance(new_status, StatusProject):
            raise ValueError('Неверный статус проекта.')

        self._status = new_status
