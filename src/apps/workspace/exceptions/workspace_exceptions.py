from src.apps.base_exception import ApplicationException


class WorkspaceException(ApplicationException):
    """Ошибка работы с рабочим пространством"""


class WorkspaceNotFound(WorkspaceException):
    """Рабочее пространство не найдено"""


class WorkspaceNotUpdated(WorkspaceException):
    """Рабочее пространство не обновлено"""


class WorkspaceNotDeleted(WorkspaceException):
    """Рабочее пространство не удалено"""


class MemberWorkspaceNotFound(WorkspaceException):
    """Участник, состоящий в рабочих пространствах, не найден"""


class WorkspaceAlreadyExists(WorkspaceException):
    """Рабочее пространство уже существует"""


class WorkspaceCreatedException(WorkspaceException):
    """Рабочее пространство не создано"""


class WorkspaceMemberNotFound(WorkspaceException):
    """Участник отсутствует в этом рабочем пространстве"""
