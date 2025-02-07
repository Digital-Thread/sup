from src.apps.base_exception import ApplicationException


class CategoryException(ApplicationException):
    """Ошибка работы с категорией"""


class CategoryNotFound(CategoryException):
    """Категория не найдена"""


class CategoryNotUpdated(CategoryException):
    """Категория не обновлена"""


class CategoryNotDeleted(CategoryException):
    """Категория не удалена"""


class WorkspaceCategoryNotFound(CategoryException):
    """Рабочее пространство для категории не найдено"""


class CategoryAlreadyExists(CategoryException):
    """Категория уже существует"""
