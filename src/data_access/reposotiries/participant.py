from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.meet.entities.participant import Participant, Status
from src.apps.meet.entities.value_objects import (
    MeetId,
    ParticipantId,
    UserId,
    WorkspaceId,
)
from src.apps.meet.repositories import (
    IParticipantRepository,
)
from src.data_access.models.meet import Participant as ParticipantModel


class ParticipantRepository(IParticipantRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = ParticipantModel

    def _map_model_to_entity(self, model: ParticipantModel) -> Participant:
        participant = Participant(
            user_id=UserId(model.user_id),
            status=Status(model.status),
        )
        participant.meet_id = MeetId(model.meet_id)
        participant.id = ParticipantId(model.id)
        return participant

    async def get_participants_by_meet_id(
        self, workspace_id: WorkspaceId, meet_id: MeetId
    ) -> list[Participant]:
        stmt = select(self.model).where(self.model.meet_id == meet_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        if not models:
            return []
        return [self._map_model_to_entity(m) for m in models]

    async def invite(self, participant: Participant) -> ParticipantId | None:
        participant_model = ParticipantModel(
            meet_id=participant.meet_id,
            user_id=participant.user_id,
            status=participant.status.value,
        )
        self._session.add(participant_model)

        participant.id = ParticipantId(participant_model.id)
        return participant.id

    async def invite_bulk(self, participants: list[Participant]) -> list[ParticipantId] | None:
        participant_models = [
            ParticipantModel(
                meet_id=p.meet_id,
                user_id=p.user_id,
                status=p.status.value,
            )
            for p in participants
        ]
        self._session.add_all(participant_models)

        for p, m in zip(participants, participant_models, strict=False):
            p.id = ParticipantId(m.id)
        return [ParticipantId(m.id) for m in participant_models]

    async def update_participant(self, participant: Participant) -> ParticipantId | None:
        participant_model = await self._session.get(self.model, participant.id)
        if not participant_model:
            return None

        participant_model.status = str(participant.status)

        await self._session.commit()
        return participant.id
