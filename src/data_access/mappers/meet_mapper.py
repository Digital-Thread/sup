from src.apps.meet.domain import (
    AssignedId,
    CategoryId,
    MeetEntity,
    MeetId,
    OwnerId,
    ParticipantEntity,
    ParticipantId,
    Status,
    UserId,
    WorkspaceId,
)
from src.data_access.models import MeetModel, ParticipantModel


class MeetMapper:
    @staticmethod
    def map_entity_to_model(meet_entity: MeetEntity) -> MeetModel:
        meet_model = MeetModel(
            workspace_id=meet_entity.workspace_id,
            name=meet_entity.name,
            meet_at=meet_entity.meet_at,
            category_id=meet_entity.category_id,
            owner_id=meet_entity.owner_id,
            assigned_to_id=meet_entity.assigned_to,
            created_at=meet_entity.created_at,
            updated_at=meet_entity.updated_at,
        )
        if meet_entity.participants:
            meet_model.participants = [
                ParticipantModel(
                    user_id=p.user_id,
                    status=p.status.value,
                )
                for p in meet_entity.participants
            ]
        return meet_model

    @staticmethod
    def map_model_to_entity(meet_model: MeetModel) -> MeetEntity:
        meet = MeetEntity(
            workspace_id=WorkspaceId(meet_model.workspace_id),
            name=meet_model.name,
            meet_at=meet_model.meet_at,
            category_id=CategoryId(meet_model.category_id),
            owner_id=OwnerId(meet_model.owner_id),
            assigned_to=AssignedId(meet_model.assigned_to_id),
        )

        meet.id = MeetId(meet_model.id)
        meet.created_at = meet_model.created_at
        meet.updated_at = meet_model.updated_at
        meet.participants = (
            [
                ParticipantEntity(
                    user_id=UserId(p.user_id),
                    status=Status(p.status),
                )
                for p in meet_model.participants
            ]
            if meet_model.participants
            else None
        )
        return meet


class MeetParticipantMapper:
    @staticmethod
    def map_entity_to_model(participant_entity: ParticipantEntity) -> ParticipantModel:
        return ParticipantModel(
            meet_id=participant_entity.meet_id,
            user_id=participant_entity.user_id,
            status=participant_entity.status.value,
        )

    @staticmethod
    def map_model_to_entity(participant_model: ParticipantModel) -> ParticipantEntity:
        participant = ParticipantEntity(
            user_id=UserId(participant_model.user_id),
            status=Status(participant_model.status),
        )
        participant.id = ParticipantId(participant_model.id)
        participant.meet_id = MeetId(participant_model.meet_id)
        return participant
