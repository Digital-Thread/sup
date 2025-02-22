from typing import Any, Tuple

from src.apps import ApplicationException
from src.apps.permission.domain import PermissionGroupId


class PermissionGroupError(ApplicationException):
    DEFAULT_MESSAGE = 'Ошибка во время работы с группой прав.'

    def __init__(
            self,
            context: Exception | None = None,
            message: str | None = None
    ) -> None:
        self.context = context
        self.message = message or self.DEFAULT_MESSAGE
        self.args: Tuple[Any, ...] = (self.context, self.message)

    def __str__(self) -> str:
        if self.context:
            return f'{self.message} {self.context}'

        return self.message


class PermissionGroupCreateError(PermissionGroupError):
    DEFAULT_MESSAGE = 'Ошибка во время создания группы прав.'


class PermissionGroupUpdateError(PermissionGroupError):
    DEFAULT_MESSAGE = 'Ошибка при обновлении группы прав.'


class PermissionGroupDeleteError(PermissionGroupError):
    DEFAULT_MESSAGE = 'Ошибка во время удаления группы прав.'


class PermissionGroupDoesNotExistError(PermissionGroupError):
    DEFAULT_MESSAGE = 'Группа прав не найдена.'

    def __init__(
            self,
            perm_group_id: PermissionGroupId | None = None,
            context: Exception | None = None,
            message: str | None = None,
    ) -> None:
        custom_message = f'Группа прав с ID {perm_group_id} не найдена.' if perm_group_id else message
        super().__init__(context=context, message=custom_message or self.DEFAULT_MESSAGE)
        self.perm_group_id = perm_group_id
        self.args = (self.perm_group_id, self.context, self.message)


class PermissionGroupRepositoryError(PermissionGroupError):
    DEFAULT_MESSAGE = 'Ошибка репозитория.'
