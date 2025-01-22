from abc import ABC, abstractmethod

from ..domain.meet import MeetEntity
from ..domain.type_ids import (
    MeetId,
)
from ..query_parameters import MeetListQuery


class IMeetRepository(ABC):
    @abstractmethod
    async def save(self, meet: MeetEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, query: MeetListQuery) -> list[MeetEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, meet_id: MeetId) -> MeetEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, meet: MeetEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, meet_id: MeetId) -> None:
        raise NotImplementedError
