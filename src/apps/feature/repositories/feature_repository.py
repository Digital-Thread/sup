from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Literal, NamedTuple, TypedDict
from uuid import UUID

from apps.feature.domain.entities.feature import Feature


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
    member: list[UUID]
    tag: list[UUID]
    status: list[int]
    project: list[UUID]


@dataclass
class FeatureListQuery:
    filters: FilterField | None = None
    order_by: SortBy[OrderByField, SortOrder] | None = SortBy(OrderByField.PRIORITY, SortOrder.DESC)
    paginate_by: Literal[5, 10] | None = 10
    page: int = 1


class FeatureRepository(ABC):

    @abstractmethod
    async def create(self, feature: Feature) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, feature_id: UUID) -> Feature | None:
        pass

    @abstractmethod
    async def update(self, feature: Feature) -> None:
        pass

    @abstractmethod
    async def delete(self, feature_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_list(self, query: FeatureListQuery) -> list[Feature]:
        pass
