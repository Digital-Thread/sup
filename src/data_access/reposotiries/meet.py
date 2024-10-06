from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.meet.entities.meet import Meet
from src.apps.meet.entities.participant import Participant, Status
from src.apps.meet.entities.value_objects import (
    AssignedId,
    CategoryId,
    MeetId,
    OwnerId,
    ParticipantId,
    UserId,
    WorkspaceId,
)
from src.apps.meet.repositories import (
    IMeetRepository,
    IParticipantRepository,
    MeetListQuery,
    SortOrder,
)
from src.data_access.models import Meet as MeetModel
from src.data_access.models.meet import Participant as ParticipantModel


class MeetRepository(IMeetRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = MeetModel

    def _map_model_to_entity(self, model: MeetModel) -> Meet:
        meet = Meet(
            name=model.name,
            workspace_id=WorkspaceId(model.workspace_id),
            owner_id=OwnerId(model.owner_id),
            meet_at=model.meet_at,
            category_id=CategoryId(model.category_id),
            assigned_to=AssignedId(model.assigned_to),
            participants=[
                Participant(
                    user_id=UserId(p.user_id),
                    status=Status(p.status),
                    meet_id=MeetId(p.meet_id),
                )
                for p in model.participants
            ],
        )
        meet.id = MeetId(model.id)
        for participant in meet.participants:
            participant.id = ParticipantId(participant.id)
        return meet

    async def create_meet(self, meet: Meet) -> MeetId | None:
        meet_model = MeetModel(
            owner_id=meet.owner_id,
            workspace_id=meet.workspace_id,
            name=meet.name,
            meet_at=meet.meet_at,
            category_id=meet.category_id,
            assigned_to=meet.assigned_to,
        )

        meet_model.participants = [
            ParticipantModel(
                user_id=p.user_id,
                status=p.status.value,
            )
            for p in meet.participants
        ]

        self._session.add(meet_model)

        meet.id = MeetId(meet_model.id)
        for participant, participant_model in zip(
            meet.participants, meet_model.participants, strict=False
        ):
            participant.id = ParticipantId(participant_model.id)
            participant.meet_id = MeetId(meet_model.id)

        return meet.id

    async def get_meets(self, workspace_id: WorkspaceId, query: MeetListQuery) -> list[Meet]:
        filters = {k: v for k, v in (query.filters or {}).items() if v is not None}
        stmt = (
            select(self.model)
            .options(selectinload(self.model.participants))
            .filter_by(workspace_id=workspace_id, **filters)
            .order_by(
                getattr(self.model, query.order_by.field.value).asc()
                if query.order_by.order == SortOrder.ASC
                else getattr(self.model, query.order_by.field.value).desc()
            )
            .limit(query.limit)
            .offset(query.offset)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._map_model_to_entity(m) for m in models] if models else []

    async def get_meet_by_id(self, workspace_id: WorkspaceId, meet_id: MeetId) -> Meet | None:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.participants))
            .where(self.model.id == meet_id, self.model.workspace_id == workspace_id)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return self._map_model_to_entity(model)
        return None

    async def update_meet(self, meet: Meet) -> MeetId | None:
        meet_model = await self._session.get(
            self.model, meet.id, options=[selectinload(self.model.participants)]
        )

        if not meet_model:
            return None

        if meet_model.workspace_id != meet.workspace_id or meet_model.owner_id != meet.owner_id:
            return None

        meet_model.name = meet.name
        meet_model.meet_at = meet.meet_at
        meet_model.category_id = meet.category_id
        meet_model.assigned_to = meet.assigned_to

        return meet.id


class ParticipantRepository(IParticipantRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = ParticipantModel

    def _map_model_to_entity(self, model: ParticipantModel) -> Participant:
        participant = Participant(
            user_id=UserId(model.user_id),
            meet_id=MeetId(model.meet_id),
            status=Status(model.status),
        )
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
