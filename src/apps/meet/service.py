from functools import wraps
from typing import Type
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
from .entities.participant import Participant, Status
from .entities.value_objects import (
    AssignedId,
    CategoryId,
    MeetId,
    OwnerId,
    ParticipantId,
    UserId,
    WorkspaceId,
)
from .exceptions import (
    AccessDeniedException,
    BaseMeetException,
    MeetCreateException,
    MeetInviteException,
    MeetNotFoundException,
    ParticipantCheckException,
    ParticipantNotFoundException,
)
from .protocols import WorkspaceServiceProtocol
from .repositories import IMeetRepository, IParticipantRepository, MeetListQuery


def check_access(method):
    @wraps(method)
    async def wrapper(self, user_id: UUID, workspace_id: int, *args, **kwargs):
        has_access = await self.workspace_service.user_has_access(user_id, workspace_id)
        if not has_access:
            raise AccessDeniedException()
        return await method(self, user_id, workspace_id, *args, **kwargs)

    return wrapper


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

    def _create_entity[T](
        self, entity_class: Type[T], data: dict, exception_class: Type[BaseMeetException]
    ) -> T:
        try:
            return entity_class(**data)
        except ValueError as e:
            raise exception_class() from e

    @check_access
    async def create_meet(self, owner_id: UUID, workspace_id: int, dto: MeetInputDTO) -> int:
        meet_data = {
            'owner_id': OwnerId(owner_id),
            'workspace_id': WorkspaceId(workspace_id),
            'name': dto.name,
            'meet_at': dto.meet_at,
            'category_id': CategoryId(dto.category_id),
            'assigned_to': AssignedId(dto.assigned_to),
            'participants': [
                {
                    'user_id': ParticipantId(dto_participant.user_id),
                    'status': Status(dto_participant.status),
                }
                for dto_participant in dto.participants
            ],
        }
        meet = self._create_entity(Meet, meet_data, MeetCreateException)
        meet_id = await self.meet_repository.create_meet(meet)
        return int(meet_id)

    @check_access
    async def get_meets(
        self, user_id: UUID, workspace_id: int, query: MeetListQueryDTO
    ) -> list[MeetResponseDTO]:
        meet_query = MeetListQuery(**query.__dict__)

        meets = await self.meet_repository.get_meets(WorkspaceId(workspace_id), meet_query)
        if not meets:
            raise MeetNotFoundException()

        return [m.to_dto() for m in meets]

    @check_access
    async def get_meet_by_id(
        self, user_id: UUID, workspace_id: int, meet_id: int
    ) -> MeetResponseDTO:
        meet = await self.meet_repository.get_meet_by_id(WorkspaceId(workspace_id), MeetId(meet_id))
        if not meet:
            raise MeetNotFoundException()

        return meet.to_dto()

    @check_access
    async def invite(self, owner_id: UUID, workspace_id: int, dto: InvitedMeetDTO) -> int:
        participant_data = {
            'meet_id': MeetId(dto.meet_id),
            'user_id': UserId(dto.user_id),
            'status': Status(dto.status),
        }
        participant = self._create_entity(Participant, participant_data, MeetInviteException)
        participant_id = await self.participant_repository.invite(participant)
        return int(participant_id)

    @check_access
    async def invite_bulk(self, owner_id: UUID, workspace_id: int, dtos: list[InvitedMeetDTO]):
        participants_data = [
            {
                'meet_id': MeetId(dto.meet_id),
                'user_id': UserId(dto.user_id),
                'status': Status(dto.status),
            }
            for dto in dtos
        ]
        participants = [
            self._create_entity(Participant, d, MeetInviteException) for d in participants_data
        ]
        participant_ids = await self.participant_repository.invite_bulk(participants)
        return participant_ids

    @check_access
    async def get_participants(
        self, user_id: UUID, workspace_id: int, meet_id: int
    ) -> list[ParticipantResponseDTO]:
        participants = await self.participant_repository.get_participants_by_meet_id(
            MeetId(meet_id)
        )
        if not participants:
            raise ParticipantNotFoundException()
        return [p.to_dto() for p in participants]

    @check_access
    async def update_participant(
        self, user_id: UUID, workspace_id: int, dto: ParticipantUpdateDTO
    ) -> int:
        participant_data = {
            'id': ParticipantId(dto.id),
            'status': Status(dto.status),
        }
        participant = self._create_entity(Participant, participant_data, ParticipantCheckException)
        participant_id = await self.participant_repository.update_participant(participant)
        return int(participant_id)
