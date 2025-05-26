from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from re import match

from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ParticipantId,
    ProjectId,
    WorkspaceId,
)


class StatusProject(Enum):
    DISCUSSION = 'В обсуждении'
    DEVELOPMENT = 'В разработке'
    SUPPORT = 'В поддержке'
    PAUSE = 'На паузе'
    CLOSED = 'Закрыт'


@dataclass
class ProjectEntity:
    _name: str
    _owner_id: OwnerId
    _workspace_id: WorkspaceId | None = field(default=None)
    _id: ProjectId | None = field(default=None)
    _description: str | None = field(default=None)
    logo: str | None = field(default=None)
    _status: StatusProject = field(default=StatusProject.DISCUSSION)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_to: AssignedId | None = field(default=None)
    participant_ids: list[ParticipantId] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_name(self._name)

        if self._description is not None:
            self._validate_description(self._description)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name.strip():
            raise ValueError(f'Имя проекта должно содержать хотя бы одну букву')

        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s]{1,20}$'
        if not bool(match(pattern, name)):
            raise ValueError(
                'Название проекта должно содержать только буквы русского и латинского алфавита.'
                'Длина не должна превышать 20 символов.'
            )

    @staticmethod
    def _validate_description(description: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s\.\-]{1,500}$'
        if not bool(match(pattern, description)):
            raise ValueError(
                f'Длина описания проекта не должна превышать 500 символов.'
                f'И содержать только буквы латинского и русского алфавитов, включая символы пробела и - .'
            )

    @property
    def id(self) -> ProjectId | None:
        return self._id

    @id.setter
    def id(self, new_id: ProjectId) -> None:
        if self._id is not None:
            raise AttributeError('Идентификатор проекта уже установлен')

        self._id = new_id

    @property
    def owner_id(self) -> OwnerId:
        return self._owner_id

    @property
    def workspace_id(self) -> WorkspaceId:
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, new_workspace_id: WorkspaceId) -> None:
        if self.workspace_id is not None:
            raise AttributeError(
                'Идентификатор рабочего пространство для этого проекта уже установлен'
            )

        self._workspace_id = new_workspace_id

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
