from src.apps.base_exception import ApplicationException


class RoleException(ApplicationException):
    pass


class RoleNotFound(RoleException):
    """Роль не найдена"""


class WorkspaceRoleNotFound(RoleException):
    """Рабочее пространство для роли не найдено"""


class RoleAlreadyExists(RoleException):
    """Роль уже существует"""
