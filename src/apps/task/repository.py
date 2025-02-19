from abc import ABC, abstractmethod

from src.apps.task.domain import FeatureId, TaskEntity, TaskId
from src.apps.task.dtos import (
    TaskAttrsWithWorkspace,
    TaskInFeatureOutputDTO,
    TaskOutputDTO,
)
from src.apps.task.query_parameters import TaskListQuery


class ITaskRepository(ABC):

    @abstractmethod
    async def save(self, task: TaskEntity) -> None:
        pass

    @abstractmethod
    async def get_entity(self, task_id: TaskId) -> TaskEntity | None:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> TaskOutputDTO | None:
        pass

    @abstractmethod
    async def update(self, task_id: TaskId, task: TaskEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, task_id: TaskId) -> None:
        pass

    @abstractmethod
    async def delete_comments(self, task_id: TaskId) -> None:
        pass

    @abstractmethod
    async def get_by_feature_id(
        self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[TaskInFeatureOutputDTO]:
        pass

    @abstractmethod
    async def validate_workspace_consistency(
        self,
        attrs: TaskAttrsWithWorkspace,
    ) -> None:
        pass
