from typing import TYPE_CHECKING

from apps.meet.entities.meet_dtos import AddMeetDTO, MeetDTO
from apps.meet.entities.participant_dtos import (
    InvitedMeetDTO,
    ParticipantMeetDTO,
    UpdateStatusParticipantMeetDTO,
)

from .exceptions import (
    MeetCreateException,
    MeetInviteException,
    MeetNotFoundException,
    ParticipantCheckException,
    ParticipantNotFoundException,
)
from .repositories import IMeetRepositoryFactory

if TYPE_CHECKING:
    from .protocols import UserServiceProtocol, WorkspaceServiceProtocol


class MeetService:
    def __init__(
        self,
        repository_factory: IMeetRepositoryFactory,
        user_service: 'UserServiceProtocol',
        workspace_service: 'WorkspaceServiceProtocol',
    ):
        self.meet_repository = repository_factory.get_meet_repository()
        self.participant_repository = repository_factory.get_participant_repository()
        self.user_service = user_service
        self.workspace_service = workspace_service

    async def get_meets(self, **filter_by: int | str) -> list[MeetDTO]:
        meets = await self.meet_repository.get_meets(**filter_by)
        return meets

    async def get_meet_by_id(self, meet_id: int) -> MeetDTO:
        meet = await self.meet_repository.get_meet_by_id(meet_id)
        if not meet:
            raise MeetNotFoundException()
        return meet

    async def add_meet(self, dto: AddMeetDTO):
        try:
            await self.meet_repository.add_meet(dto)
        except ValueError as e:
            raise MeetCreateException() from e

    async def invite(self, meet_id: int, dto: InvitedMeetDTO):
        await self.get_meet_by_id(meet_id)
        try:
            await self.participant_repository.invite(meet_id, dto)
        except ValueError as e:
            raise MeetInviteException() from e

    async def get_participants(self, meet_id: int) -> list[ParticipantMeetDTO]:
        await self.get_meet_by_id(meet_id)
        participants = await self.participant_repository.get_participants_by_meet_id(meet_id)
        if not participants:
            raise ParticipantNotFoundException()
        return participants

    async def check_participation(self, meet_id, dto: UpdateStatusParticipantMeetDTO):
        try:
            await self.participant_repository.check_participant(meet_id, dto)
        except ValueError as e:
            raise ParticipantCheckException() from e
