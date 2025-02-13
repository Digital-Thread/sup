from abc import ABC, abstractmethod

from src.apps.task.query_parameters import TaskListQuery
from src.apps.task.domain import FeatureId, TaskEntity, TaskId


class ITaskRepository(ABC):

    @abstractmethod
    async def save(self, task: TaskEntity) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> TaskEntity | None:
        pass

    @abstractmethod
    async def update(self, task_id: TaskId, task: TaskEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, task_id: TaskId) -> None:
        pass

    @abstractmethod
    async def get_list(
            self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[TaskEntity]:
        pass
