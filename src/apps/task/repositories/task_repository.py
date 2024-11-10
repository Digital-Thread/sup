from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Literal, NamedTuple

from src.apps.task.domain import FeatureId, Task, TaskId


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to_id'
    DUE_DATE = 'due_date'
    CREATED_AT = 'created_at'
    PRIORITY = 'priority'
    STATUS = 'status'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class OrderBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class PaginateParams(NamedTuple):
    offset: int
    limit_by: Literal[5, 10, None]


@dataclass
class TaskListQuery:
    order_by: OrderBy | None = OrderBy(OrderByField.PRIORITY, SortOrder.DESC)
    paginate_by: PaginateParams = PaginateParams(offset=0, limit_by=10)


class ITaskRepository(ABC):

    @abstractmethod
    async def save(self, task: Task) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> Task | None:
        pass

    @abstractmethod
    async def update(self, task_id: TaskId, task: Task) -> None:
        pass

    @abstractmethod
    async def delete(self, task_id: TaskId) -> None:
        pass

    @abstractmethod
    async def get_list(
            self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[tuple[TaskId, Task]]:
        pass
