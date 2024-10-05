from uuid import UUID

from .dtos import (
    InvitedMeetDTO,
    MeetInputDTO,
    MeetListQueryDTO,
    MeetResponseDTO,
    ParticipantResponseDTO,
    ParticipantUpdateDTO,
)
from .entities.meet import Meet
from .entities.participant import Participant
from .entities.value_objects import MeetId, OwnerId, WorkspaceId
from .exceptions import (
    AccessDeniedException,
    MeetCreateException,
    MeetInviteException,
    MeetNotFoundException,
    ParticipantCheckException,
    ParticipantNotFoundException,
)
from .protocols import WorkspaceServiceProtocol
from .repositories import IMeetRepository, IParticipantRepository, MeetListQuery


class MeetService:
    def __init__(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
        workspace_service: WorkspaceServiceProtocol,
    ):
        self.meet_repository = meet_repository
        self.participant_repository = participant_repository
        self.workspace_service = workspace_service

    async def create_meet(self, owner_id: UUID, workspace_id: int, dto: MeetInputDTO) -> int:
        has_access = await self.workspace_service.user_has_access(owner_id, workspace_id)

        if not has_access:
            raise AccessDeniedException()

        try:
            meet = Meet(**dto.__dict__)
            owner_id_ = OwnerId(owner_id)
            workspace_id_ = WorkspaceId(workspace_id)
        except ValueError as e:
            raise MeetCreateException() from e

        meet_id = await self.meet_repository.create_meet(owner_id_, workspace_id_, meet)
        return int(meet_id)

    async def get_meets(
        self, user_id: UUID, workspace_id: int, query: MeetListQueryDTO
    ) -> list[MeetResponseDTO]:
        has_access = await self.workspace_service.user_has_access(user_id, workspace_id)

        if not has_access:
            raise AccessDeniedException()

        meet_query = MeetListQuery(**query.__dict__)
        workspace_id_ = WorkspaceId(workspace_id)

        meets = await self.meet_repository.get_meets(workspace_id_, meet_query)
        if not meets:
            raise MeetNotFoundException()

        return [MeetResponseDTO(**m.__dict__) for m in meets]

    async def get_meet_by_id(
        self, user_id: UUID, workspace_id: int, meet_id: int
    ) -> MeetResponseDTO:
        has_access = await self.workspace_service.user_has_access(user_id, workspace_id)

        if not has_access:
            raise AccessDeniedException()

        meet = await self.meet_repository.get_meet_by_id(WorkspaceId(workspace_id), MeetId(meet_id))
        if not meet:
            raise MeetNotFoundException()

        return MeetResponseDTO(**meet.__dict__)

    async def invite(self, owner_id: UUID, workspace_id: int, dto: InvitedMeetDTO):
        has_access = await self.workspace_service.user_has_access(owner_id, workspace_id)

        if not has_access:
            raise AccessDeniedException()

        try:
            participant = Participant(**dto.__dict__)
            workspace_id_ = WorkspaceId(workspace_id)
        except ValueError as e:
            raise MeetInviteException() from e

        await self.participant_repository.invite(workspace_id_, participant)

    async def get_participants(
        self, user_id: UUID, workspace_id: int, meet_id: int
    ) -> list[ParticipantResponseDTO]:
        has_access = await self.workspace_service.user_has_access(user_id, workspace_id)

        if not has_access:
            raise AccessDeniedException()

        participants = await self.participant_repository.get_participants_by_meet_id(
            WorkspaceId(workspace_id), MeetId(meet_id)
        )
        if not participants:
            raise ParticipantNotFoundException()
        return [ParticipantResponseDTO(**p.__dict__) for p in participants]

    async def update_participant(
        self, user_id: UUID, workspace_id: int, dto: ParticipantUpdateDTO
    ) -> int:
        has_access = await self.workspace_service.user_has_access(user_id, workspace_id)

        if not has_access:
            raise AccessDeniedException()

        try:
            participant = Participant(**dto.__dict__)
            workspace_id_ = WorkspaceId(workspace_id)
        except ValueError as e:
            raise ParticipantCheckException() from e

        return await self.participant_repository.update_participant(workspace_id_, participant)
