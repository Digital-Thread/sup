from typing import Any, Tuple

from src.apps import ApplicationException
from src.apps.task.domain import TaskId


class TaskError(ApplicationException):
    DEFAULT_MESSAGE = 'Ошибка во время работы с задачей.'

    def __init__(
        self,
        context: Exception = None,
        message: str = None,
    ) -> None:
        self.context = context
        self.message = message or self.DEFAULT_MESSAGE
        self.args: Tuple[Any, ...] = (self.context, self.message)

    def __str__(self) -> str:
        if self.context:
            return f'{self.message} {self.context}'

        return self.message


class TaskCreateError(TaskError):
    DEFAULT_MESSAGE = 'Ошибка во время создания задачи.'


class TaskUpdateError(TaskError):
    DEFAULT_MESSAGE = 'Ошибка при обновлении задачи.'


class TaskDeleteError(TaskError):
    DEFAULT_MESSAGE = 'Ошибка во время удаления задачи.'


class TaskDoesNotExistError(TaskError):
    DEFAULT_MESSAGE = 'Задача не найдена.'

    def __init__(
        self,
        task_id: TaskId = None,
        context: Exception = None,
        message: str = None,
    ) -> None:
        custom_message = f'Задача с ID {task_id} не найдена.' if task_id else message
        super().__init__(context=context, message=custom_message or self.DEFAULT_MESSAGE)
        self.task_id = task_id
        self.args = (self.task_id, self.context, self.message)


class TaskRepositoryError(TaskError):
    DEFAULT_MESSAGE = 'Ошибка репозитория.'
