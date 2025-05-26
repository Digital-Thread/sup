from src.apps.base_exception import ApplicationException


class ProjectException(ApplicationException):
    """Ошибка работы с проектом"""


class ProjectNotFound(ProjectException):
    """Проект не найден"""


class ProjectNotUpdated(ProjectException):
    """Проект не обновлен"""


class ProjectNotDeleted(ProjectException):
    """Проект не удален"""


class WorkspaceForProjectNotFound(ProjectException):
    """Рабочее пространство для проекта не найдено"""


class ProjectAlreadyExists(ProjectException):
    """Проект уже существует"""


class ParticipantNotFound(ProjectException):
    """Участник не найден"""
