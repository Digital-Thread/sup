from abc import ABC, abstractmethod
from typing import Any

from src.apps.task.repository import ITaskRepository


class BaseInteractor(ABC):
    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    @abstractmethod
    async def execute(self, *args: Any) -> Any: ...
