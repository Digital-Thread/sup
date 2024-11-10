from functools import wraps
from typing import Any, Awaitable, Callable, Concatenate, ParamSpec, Type, TypeVar
from uuid import UUID

from .dtos import (
    MeetCreateDTO,
    MeetListQueryDTO,
    MeetResponseDTO,
    MeetUpdateDTO,
    ParticipantCreateDTO,
    ParticipantDeleteDTO,
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
    MeetNotFoundException,
    ParticipantCreateException,
    ParticipantNotFoundException,
)
from .protocols import WorkspaceServiceProtocol
from .repositories import IMeetRepository, IParticipantRepository, MeetListQuery

P = ParamSpec('P')
R = TypeVar('R')


def check_access(
    method: Callable[Concatenate[Any, UUID, UUID, P], Awaitable[R]],
) -> Callable[Concatenate[Any, UUID, UUID, P], Awaitable[R]]:
    @wraps(method)
    async def wrapper(
        self: Any, user_id: UUID, workspace_id: UUID, *args: P.args, **kwargs: P.kwargs
    ) -> R:
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

    @check_access
    async def create_meet(self, owner_id: UUID, workspace_id: UUID, dto: MeetCreateDTO) -> None:
        """
        Create a new meet

        Args:
            owner_id: The ID of the user who creates the meet
            workspace_id: The ID of the workspace where the meet takes place
            dto: The data transfer object with the meet's data

        """
        meet_data = {
            'owner_id': OwnerId(owner_id),
            'workspace_id': WorkspaceId(workspace_id),
            'name': dto.name,
            'meet_at': dto.meet_at,
            'category_id': CategoryId(dto.category_id),
            'assigned_to': AssignedId(dto.assigned_to),
            'participants': [
                self._create_entity(
                    Participant,
                    {
                        'user_id': UserId(dto_participant.user_id),
                        'status': Status(dto_participant.status),
                    },
                    ParticipantCreateException,
                )
                for dto_participant in dto.participants
            ],
        }
        meet = self._create_entity(Meet, meet_data, MeetCreateException)
        await self.meet_repository.create_meet(meet)

    @check_access
    async def get_meets(
        self, user_id: UUID, workspace_id: int, query: MeetListQueryDTO
    ) -> list[MeetResponseDTO]:
        """
        Get a list of meetings for a given workspace.

        Args:
            user_id: The ID of the user who is requesting the list of meetings.
            workspace_id: The ID of the workspace that the meetings belong to.
            query: A query object that contains the filters and ordering for the list of meetings.

        Returns:
            A list of MeetResponseDTO objects, each representing a meeting in the given workspace.
        """
        meet_query = MeetListQuery(**query.__dict__)

        meets = await self.meet_repository.get_meets(WorkspaceId(workspace_id), meet_query)
        if not meets:
            raise MeetNotFoundException()

        return [m.to_dto() for m in meets]

    @check_access
    async def get_meet_by_id(
        self, user_id: UUID, workspace_id: int, meet_id: int
    ) -> MeetResponseDTO:
        """
        Get a meet by its id.

        Args:
            user_id: The UUID of the user making the request.
            workspace_id: The id of the workspace that the meet belongs to.
            meet_id: The id of the meet to retrieve.

        Returns:
            A MeetResponseDTO containing the meet's data.

        Raises:
            MeetNotFoundException: If the meet does not exist.
        """
        meet = await self._get_meet_or_raise(workspace_id, meet_id)

        return meet.to_dto()

    @check_access
    async def update_meet(
        self, user_id: UUID, workspace_id: int, meet_id: int, dto: MeetUpdateDTO
    ) -> None:
        """
        Update a meet.

        Args:
            user_id: The UUID of the user making the request.
            workspace_id: The id of the workspace that the meet belongs to.
            meet_id: The id of the meet to update.
            dto: A MeetUpdateDTO containing the updated data for the meet.

        Raises:
            MeetNotFoundException: If the meet does not exist.
            AccessDeniedException: If the user is not the owner of the meet.
        """
        meet = await self._get_meet_or_raise(workspace_id, meet_id)

        if meet.owner_id != user_id:
            raise AccessDeniedException()

        await self._update_meet_fields(meet, dto)

        await self._process_participant_updates(dto, meet)

    @check_access
    async def delete_meet(self, user_id: UUID, workspace_id: int, meet_id: int) -> None:
        """
        Delete a meet.

        Args:
            user_id: The UUID of the user making the request.
            workspace_id: The id of the workspace that the meet belongs to.
            meet_id: The id of the meet to delete.

        Raises:
            MeetNotFoundException: If the meet does not exist.
            AccessDeniedException: If the user is not the owner of the meet.
        """
        meet = await self._get_meet_or_raise(workspace_id, meet_id)

        if meet.owner_id != user_id:
            raise AccessDeniedException()

        await self.meet_repository.delete_meet(MeetId(meet_id))

    @check_access
    async def get_participants(
        self, user_id: UUID, workspace_id: int, meet_id: int
    ) -> list[ParticipantResponseDTO]:
        participants = await self.participant_repository.get_participants_by_meet_id(
            WorkspaceId(workspace_id), MeetId(meet_id)
        )

        if not participants:
            raise ParticipantNotFoundException()

        return [p.to_dto() for p in participants]

    @check_access
    async def update_participant(
        self, user_id: UUID, workspace_id: int, dto: ParticipantUpdateDTO
    ) -> int:
        participant = await self._get_participant_or_raise(dto.id)
        if dto.status is not None:
            participant.status = Status(dto.status)
        participant_id = await self.participant_repository.update_participant(participant)
        return int(participant_id)

    def _create_entity[T](
        self, entity_class: Type[T], data: dict[str, Any], exception_class: Type[BaseMeetException]
    ) -> T:
        try:
            return entity_class(**data)
        except ValueError as e:
            raise exception_class() from e

    async def _get_meet_or_raise(self, workspace_id: int, meet_id: int) -> Meet:
        meet = await self.meet_repository.get_meet_by_id(WorkspaceId(workspace_id), MeetId(meet_id))
        if not meet:
            raise MeetNotFoundException()
        return meet

    async def _get_participant_or_raise(self, participant_id: int) -> Participant:
        participant = await self.participant_repository.get_participant_by_id(
            ParticipantId(participant_id)
        )
        if not participant:
            raise ParticipantNotFoundException()
        return participant

    async def _update_meet_fields(self, meet: Meet, dto: MeetUpdateDTO) -> None:
        if dto.name is not None:
            meet.name = dto.name
        if dto.meet_at is not None:
            meet.meet_at = dto.meet_at
        if dto.category_id is not None:
            meet.category_id = CategoryId(dto.category_id)
        if dto.assigned_to is not None:
            meet.assigned_to = AssignedId(dto.assigned_to)

        await self.meet_repository.update_meet(meet)

    async def _process_participant_updates(self, dto: MeetUpdateDTO, meet: Meet) -> None:
        await self._add_new_participants(dto.participants_to_add, meet)

        await self._update_existing_participants(dto.participants_to_update)

        await self._delete_participants(dto.participants_to_delete)

    async def _add_new_participants(
        self, participants_to_add: list[ParticipantCreateDTO], meet: Meet
    ) -> None:
        for participant_dto in participants_to_add:
            participant = Participant(
                user_id=UserId(participant_dto.user_id),
                status=Status(participant_dto.status),
            )
            participant.meet_id = meet.id
            await self.participant_repository.add_participant(participant)

    async def _update_existing_participants(
        self, participants_to_update: list[ParticipantUpdateDTO]
    ) -> None:
        for participant_dto in participants_to_update:
            participant = await self.participant_repository.get_participant_by_id(
                ParticipantId(participant_dto.id)
            )
            if participant:
                participant.status = Status(participant_dto.status)
                await self.participant_repository.update_participant(participant)
            else:
                raise ParticipantNotFoundException()

    async def _delete_participants(
        self, participants_to_delete: list[ParticipantDeleteDTO]
    ) -> None:
        for participant_dto in participants_to_delete:
            await self.participant_repository.delete_participant(ParticipantId(participant_dto.id))
