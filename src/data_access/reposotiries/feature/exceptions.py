from apps import ApplicationException


class DataBaseError(ApplicationException):
    """Сохраняет и передаёт detail_message из ForeignKeyViolationError выше"""
