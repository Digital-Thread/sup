from src.apps.base_exception import ApplicationException


class ProjectException(ApplicationException):
    """Ошибка работы с категорией"""


class ProjectNotFound(ProjectException):
    """Категория не найдена"""


class ProjectNotUpdated(ProjectException):
    """Категория не обновлена"""


class WorkspaceForProjectNotFound(ProjectException):
    """Рабочее пространство для категории не найдено"""


class ProjectAlreadyExists(ProjectException):
    """Категория уже существует"""


class ParticipantNotFound(ProjectException):
    """Участник не найден"""
