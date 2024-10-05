from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def create_meet(
        self, owner_id: OwnerId, workspace_id: WorkspaceId, meet: Meet
    ) -> MeetId | None:
        try:
            stmt = (
                insert(self.model)
                .values(owner_id=owner_id, workspace_id=workspace_id, **meet.__dict__)
                .returning(self.model.id)
            )
            result = await self._session.execute(stmt)
            await self._session.commit()
            return MeetId(result.scalar_one()) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_meets(self, workspace_id: WorkspaceId, query: MeetListQuery) -> list[Meet]:
        filters = {k: v for k, v in query.filters.__dict__.items() if v is not None}
        stmt = (
            select(self.model)
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
        if not result:
            return []
        models = result.scalars().all()
        return [self._map_model_to_entity(m) for m in models] if models else []

    async def get_meet_by_id(self, workspace_id: WorkspaceId, meet_id: MeetId) -> Meet | None:
        stmt = select(self.model).where(
            self.model.id == meet_id, self.model.workspace_id == workspace_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return self._map_model_to_entity(model)
        return None

    async def update_meet(
        self, owner_id: OwnerId, workspace_id: WorkspaceId, meet: Meet
    ) -> MeetId | None:
        try:
            stmt = (
                update(self.model)
                .where(
                    self.model.id == meet.id,
                    self.model.workspace_id == workspace_id,
                    self.model.owner_id == owner_id,
                )
                .values(**meet.__dict__)
                .returning(self.model)
            )
            result = await self._session.execute(stmt)
            await self._session.commit()
            return MeetId(result.scalar_one().id) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e


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
        data = result.mappings().all()
        if not data:
            return []
        return [Participant(**d) for d in data]

    async def invite(self, meet_id: MeetId, participant: Participant) -> ParticipantId | None:
        try:
            stmt = insert(self.model).values(**participant.__dict__).returning(self.model.id)
            result = await self._session.execute(stmt)
            await self._session.commit()
            return ParticipantId(result.scalar_one()) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def invite_bulk(self, participants: list[Participant]) -> list[ParticipantId] | None:
        try:
            stmt = insert(self.model).values(participants).returning(self.model.id)
            result = await self._session.execute(stmt)
            await self._session.commit()
            return [ParticipantId(r[0]) for r in result] if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def update_participant(self, participant: Participant) -> ParticipantId | None:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == participant.id)
                .values(**participant.__dict__)
                .returning(self.model)
            )
            result = await self._session.execute(stmt)
            await self._session.commit()
            return ParticipantId(result.scalar_one().id) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e
