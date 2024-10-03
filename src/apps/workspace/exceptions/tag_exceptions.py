from src.apps.base_exception import ApplicationException


class TagException(ApplicationException):
    pass


class TagNotFound(TagException):
    """Тег не найден"""

    pass


class WorkspaceTagNotFound(TagException):
    """Рабочее пространство для тега не найдено"""

    pass


class TagAlreadyExists(TagException):
    """Тег уже существует"""
