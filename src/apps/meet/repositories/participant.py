from abc import ABC, abstractmethod

from ..domain.meet import ParticipantEntity
from ..domain.type_ids import MeetId, ParticipantId


class IParticipantRepository(ABC):
    @abstractmethod
    async def save(self, participant: ParticipantEntity) -> ParticipantId:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, participant_id: ParticipantId) -> ParticipantEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, meet_id: MeetId) -> list[ParticipantEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, participant: ParticipantEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, participant_id: ParticipantId) -> None:
        raise NotImplementedError
