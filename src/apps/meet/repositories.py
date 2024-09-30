from abc import ABC, abstractmethod

from src.apps.meet.entities.meet_dtos import MeetInputDTO, MeetResponseDTO
from src.apps.meet.entities.participant_dtos import (
    InvitedMeetDTO,
    ParticipantMeetDTO,
    UpdateStatusParticipantMeetDTO,
)

from .temp_dtos import UserInputDTO, WorkspaceInputDTO


class IMeetRepository(ABC):
    @abstractmethod
    async def get_meets(
        self, workspace: WorkspaceInputDTO, owner: UserInputDTO, **filter_by: str | int
    ) -> list[MeetResponseDTO] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_meet_by_id(
        self, workspace: WorkspaceInputDTO, owner: UserInputDTO, id_: int
    ) -> MeetResponseDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def add_meet(
        self, workspace: WorkspaceInputDTO, owner: UserInputDTO, dto: MeetInputDTO
    ) -> int:
        raise NotImplementedError


class IParticipantRepository(ABC):
    @abstractmethod
    async def get_participants_by_meet_id(self, meet_id: int) -> list[ParticipantMeetDTO] | None:
        raise NotImplementedError

    @abstractmethod
    async def invite(self, meet_id: int, dto: InvitedMeetDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_participant(self, meet_id: int, dto: UpdateStatusParticipantMeetDTO) -> None:
        raise NotImplementedError
