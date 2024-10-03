from src.apps.base_exception import ApplicationException


class WorkspaceException(ApplicationException):
    pass


class WorkspaceNotFound(WorkspaceException):
    """Рабочее пространство не найдено"""

    pass


class OwnerWorkspaceNotFound(WorkspaceException):
    """Владелец рабочего пространства не найден"""

    pass


class WorkspaceAlreadyExists(WorkspaceException):
    """Рабочее пространство уже существует"""

    pass
