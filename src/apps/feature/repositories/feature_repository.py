from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Literal, NamedTuple, TypedDict

from apps.feature.domain.entities.feature import Feature
from apps.feature.domain.value_objects import FeatureId, ProjectId, TagId, UserId


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to'
    CREATED_AT = 'created_at'
    PRIORITY = 'priority'
    PROJECT = 'project'
    STATUS = 'status'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SortBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class FilterField(TypedDict, total=False):
    member: list[UserId]
    tag: list[TagId]
    status: list[int]
    project: list[ProjectId]


@dataclass
class FeatureListQuery:
    filters: FilterField | None = None
    order_by: SortBy | None = SortBy(OrderByField.PRIORITY, SortOrder.DESC)
    paginate_by: Literal[5, 10] | None = 10
    page: int = 1


class IFeatureRepository(ABC):

    @abstractmethod
    async def create(self, feature: Feature) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, feature_id: FeatureId) -> Feature | None:
        pass

    @abstractmethod
    async def update(self, feature: Feature) -> None:
        pass

    @abstractmethod
    async def delete(self, feature_id: FeatureId) -> None:
        pass

    @abstractmethod
    async def get_list(self, query: FeatureListQuery) -> list[Feature]:
        pass
