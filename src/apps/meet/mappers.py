from src.apps.meet.domain.type_ids import OwnerId

from .domain import (
    AssignedId,
    CategoryId,
    MeetEntity,
    ParticipantEntity,
    Status,
    UserId,
    WorkspaceId,
)
from .dtos import MeetInputDTO, MeetOutputDTO, ParticipantInputDTO, ParticipantOutputDTO


class MeetMapper:
    @staticmethod
    def entity_to_dto(entity: MeetEntity) -> MeetOutputDTO:
        return MeetOutputDTO(
            id=entity.id,
            owner_id=entity.owner_id,
            name=entity.name,
            meet_at=entity.meet_at,
            category_id=entity.category_id,
            assigned_to=entity.assigned_to,
            participants=[ParticipantMapper.entity_to_dto(p) for p in entity.participants]
            if entity.participants
            else None,
        )

    @staticmethod
    def dto_to_entity(dto: MeetInputDTO) -> MeetEntity:
        return MeetEntity(
            workspace_id=WorkspaceId(dto.workspace_id),
            name=dto.name,
            meet_at=dto.meet_at,
            category_id=CategoryId(dto.category_id),
            owner_id=OwnerId(dto.owner_id),
            assigned_to=AssignedId(dto.assigned_to),
            participants=[ParticipantMapper.dto_to_entity(p) for p in dto.participants]
            if dto.participants
            else None,
        )


class ParticipantMapper:
    @staticmethod
    def entity_to_dto(entity: ParticipantEntity) -> ParticipantOutputDTO:
        return ParticipantOutputDTO(
            id=entity.id,
            user_id=entity.user_id,
            status=entity.status,
            meet_id=entity.meet_id,
        )

    @staticmethod
    def dto_to_entity(dto: ParticipantInputDTO) -> ParticipantEntity:
        return ParticipantEntity(
            user_id=UserId(dto.user_id),
            status=Status(dto.status),
        )
