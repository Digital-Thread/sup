from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, TypedDict

from .entities.meet import Meet
from .entities.participant import Participant
from .entities.value_objects import AssignedId, CategoryId, MeetId, ParticipantId


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to'
    CREATED_AT = 'created_at'
    MEET_AT = 'meet_at'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SortBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class MeetFilterFields(TypedDict, total=False):
    category: CategoryId
    assigned_to: AssignedId
    meet_at: datetime


@dataclass
class MeetListQuery:
    filters: MeetFilterFields | None = None
    order_by: SortBy | None = SortBy(OrderByField.MEET_AT, SortOrder.DESC)
    paginate_by: Literal[5, 10] | None = 10
    page: int = 1


class IMeetRepository(ABC):
    @abstractmethod
    async def create_meet(self, meet: Meet) -> MeetId:
        raise NotImplementedError

    @abstractmethod
    async def get_meets(self, query: MeetListQuery) -> list[Meet] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_meet_by_id(self, meet_id: MeetId) -> Meet | None:
        raise NotImplementedError

    @abstractmethod
    async def update_meet(self, meet: Meet) -> Meet:
        raise NotImplementedError


class IParticipantRepository(ABC):
    @abstractmethod
    async def get_participants_by_meet_id(self, meet_id: MeetId) -> list[Participant] | None:
        raise NotImplementedError

    @abstractmethod
    async def invite(self, participant: Participant) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def update_participant(self, participant: Participant) -> ParticipantId:
        raise NotImplementedError
