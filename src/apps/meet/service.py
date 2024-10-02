from .dtos import MeetInputDTO, MeetResponseDTO
from .entities.participant_dtos import (
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
from .temp_dtos import UserInputDTO, WorkspaceInputDTO


class MeetService:
    def __init__(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
    ):
        self.meet_repository = meet_repository
        self.participant_repository = participant_repository

    async def get_meets(
        self, workspace: WorkspaceInputDTO, owner: UserInputDTO, **filter_by: int | str
    ) -> list[MeetResponseDTO]:
        meets = await self.meet_repository.get_meets(workspace, owner, **filter_by)
        if not meets:
            raise MeetNotFoundException()
        return meets

    async def get_meet_by_id(
        self, workspace: WorkspaceInputDTO, owner: UserInputDTO, meet_id: int
    ) -> MeetResponseDTO:
        meet = await self.meet_repository.get_meet_by_id(workspace, owner, meet_id)
        if not meet:
            raise MeetNotFoundException()
        return meet

    async def add_meet(self, workspace: WorkspaceInputDTO, owner: UserInputDTO, dto: MeetInputDTO):
        try:
            await self.meet_repository.add_meet(workspace, owner, dto)
        except ValueError as e:
            raise MeetCreateException() from e

    async def invite(self, meet_id: int, dto: InvitedMeetDTO):
        # await self.get_meet_by_id(meet_id)
        try:
            await self.participant_repository.invite(meet_id, dto)
        except ValueError as e:
            raise MeetInviteException() from e

    async def get_participants(self, meet_id: int) -> list[ParticipantMeetDTO]:
        # await self.get_meet_by_id(meet_id)
        participants = await self.participant_repository.get_participants_by_meet_id(meet_id)
        if not participants:
            raise ParticipantNotFoundException()
        return participants

    async def check_participation(self, meet_id, dto: UpdateStatusParticipantMeetDTO):
        try:
            await self.participant_repository.check_participant(meet_id, dto)
        except ValueError as e:
            raise ParticipantCheckException() from e
