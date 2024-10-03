from src.apps.base_exception import ApplicationException


class WorkspaceInviteException(ApplicationException):
    pass


class WorkspaceInviteNotFound(WorkspaceInviteException):
    """Ссылка приглашения не найдена"""

    pass


class WorkspaceWorkspaceInviteNotFound(WorkspaceInviteException):
    """Рабочее пространство для ссылки приглашения не найдено"""

    pass


class WorkspaceInviteAlreadyExists(WorkspaceInviteException):
    """Ссылка приглашения уже существует"""

    pass
