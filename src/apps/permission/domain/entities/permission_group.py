from re import match
from typing import TypedDict

from src.apps.permission.domain.types_ids import (
    PermissionId,
    PermissionGroupId,
    WorkspaceId,
    UserId,
)


class OptionalPermissionGroupUpdateFields(TypedDict, total=False):
    name: str
    description: str | None
    permissions: set[PermissionId]
    authorized_users: set[UserId] | None


class PermissionGroupEntity:

    def __init__(
            self,
            name: str,
            permissions: set[PermissionId],
            is_global: bool = False,
            workspace_id: WorkspaceId | None = None,
            description: str | None = None,
            authorized_users: set[UserId] | None = None,
    ) -> None:
        self._id: PermissionGroupId | None = None
        self.is_global = is_global
        self.workspace_id = workspace_id
        self.name = name
        self.description = description
        self.permissions = permissions
        self.authorized_users = authorized_users

    @property
    def id(self) -> PermissionGroupId | None:
        return self._id

    @id.setter
    def id(self, _id: PermissionGroupId) -> None:
        if self.id is not None:
            raise AttributeError('Идентификатор группы уже установлен')
        self._id = _id

    @property
    def workspace_id(self) -> WorkspaceId | None:
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, _id: WorkspaceId | None) -> None:
        if not self.is_global and _id is None:
            raise ValueError('Укажите ID рабочего пространства.')
        self._workspace_id = _id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._validate_name(value=value)
        self._name = value

    @staticmethod
    def _validate_name(value: str) -> None:
        max_length = 20
        pattern = r'^[a-zA-Zа-яА-ЯёЁ ]+$'
        if not value:
            raise ValueError('Название не должно быть пустым.')
        if not match(pattern, value):
            raise ValueError('Название может содержать только латиницу или кириллицу.')
        if len(value) > max_length:
            raise ValueError(f'В названии может быть максимум {max_length} символов.')

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        self._validate_description(value=value)
        self._description = value

    @staticmethod
    def _validate_description(value: str | None) -> None:
        max_length = 500
        if value is not None and len(value) > max_length:
            raise ValueError(f'В описании может быть максимум {max_length} символов.')

    @property
    def authorized_users(self) -> set[UserId]:
        return self._authorized_users

    @authorized_users.setter
    def authorized_users(self, users: set[UserId] | None) -> None:
        if users is None:
            users = set()
        self._authorized_users = users

    def update_fields(self, updates: OptionalPermissionGroupUpdateFields) -> None:
        required_fields = {
            'name': 'Название',
            'permissions': 'Разрешения для группы',
        }
        for field, value in updates.items():
            if field in required_fields.keys() and value is None:
                raise ValueError(
                    f'{required_fields[field]} обязательное поле и не может быть пустым!'
                )
            setattr(self, field, value)
