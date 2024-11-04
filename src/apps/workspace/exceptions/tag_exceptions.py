from src.apps.base_exception import ApplicationException


class TagException(ApplicationException):
    """Ошибка работы с тегом"""


class TagNotFound(TagException):
    """Тег не найден"""


class TagNotUpdated(TagException):
    """Тег не обновлен"""


class TagNotDeleted(TagException):
    """Тег не удален"""


class WorkspaceTagNotFound(TagException):
    """Рабочее пространство для тега не найдено"""


class TagAlreadyExists(TagException):
    """Тег уже существует"""


class TagCreatedException(TagException):
    """Тег не создан"""
