from src.apps.base_exception import ApplicationException


class CategoryException(ApplicationException):
    pass


class CategoryNotFound(CategoryException):
    """Категория не найдена"""


class WorkspaceCategoryNotFound(CategoryException):
    """Рабочее пространство для категории не найдено"""


class CategoryAlreadyExists(CategoryException):
    """Категория уже существует"""
