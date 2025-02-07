from src.apps.base_exception import ApplicationException


class RoleException(ApplicationException):
    """Ошибка работы с ролью"""


class RoleNotFound(RoleException):
    """Роль не найдена"""


class RoleNotUpdated(RoleException):
    """Роль не обновлена"""


class RoleNotDeleted(RoleException):
    """Роль не удалена"""


class WorkspaceRoleNotFound(RoleException):
    """Рабочее пространство для роли не найдено"""


class RoleAlreadyExists(RoleException):
    """Роль уже существует"""


class RoleCreatedException(RoleException):
    """Роль не создана"""

class RoleNotFoundForWorkspaceMember(RoleException):
    """Роль для участника рабочего пространства не найдена"""