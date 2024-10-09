from src.apps.base_exception import ApplicationException


class WorkspaceInviteException(ApplicationException):
    """Ошибка работы со ссылкой приглашения"""


class WorkspaceInviteNotFound(WorkspaceInviteException):
    """Ссылка приглашения не найдена"""


class WorkspaceInviteNotUpdated(WorkspaceInviteException):
    """Ссылка приглашения не обновлена"""


class WorkspaceInviteNotDeleted(WorkspaceInviteException):
    """Ссылка приглашения не удалена"""


class WorkspaceWorkspaceInviteNotFound(WorkspaceInviteException):
    """Рабочее пространство для ссылки приглашения не найдено"""


class WorkspaceInviteAlreadyExists(WorkspaceInviteException):
    """Ссылка приглашения уже существует"""


class WorkspaceInviteCreatedException(WorkspaceInviteException):
    """Ссылка приглашения не создана"""
