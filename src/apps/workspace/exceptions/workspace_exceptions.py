from src.apps.base_exception import ApplicationException


class WorkspaceException(ApplicationException):
    """Ошибка работы с рабочим пространством"""


class WorkspaceNotFound(WorkspaceException):
    """Рабочее пространство не найдено"""


class WorkspaceNotUpdated(WorkspaceException):
    """Рабочее пространство не обновлено"""


class WorkspaceNotDeleted(WorkspaceException):
    """Рабочее пространство не удалено"""


class OwnerWorkspaceNotFound(WorkspaceException):
    """Владелец рабочего пространства не найден"""


class WorkspaceAlreadyExists(WorkspaceException):
    """Рабочее пространство уже существует"""


class WorkspaceCreatedException(WorkspaceException):
    """Рабочее пространство не создано"""
