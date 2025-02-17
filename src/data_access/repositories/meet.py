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
from src.apps.meet.repositories import IMeetRepository, MeetListQuery
from src.data_access.models.meet import MeetModel, ParticipantModel


class MeetRepository(IMeetRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = MeetModel

    def _map_model_to_entity(self, model: MeetModel) -> Meet:
        participants = []
        for p in model.participants:
            participant = Participant(
                user_id=UserId(p.user_id),
                status=Status(p.status),
            )
            participant.id = ParticipantId(p.id)
            participant.meet_id = MeetId(model.id)
            participants.append(participant)

        meet = Meet(
            name=model.name,
            workspace_id=WorkspaceId(model.workspace_id),
            owner_id=OwnerId(model.owner_id),
            meet_at=model.meet_at,
            category_id=CategoryId(model.category_id),
            assigned_to=AssignedId(model.assigned_to),
            participants=participants,
        )
        meet.id = MeetId(model.id)
        return meet

    async def create_meet(self, meet: Meet) -> None:
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

    async def get_meets(self, workspace_id: WorkspaceId, query: MeetListQuery) -> list[Meet]:
        filters = {k: v for k, v in (query.filters or {}).items() if v is not None}
        stmt = (
            select(self.model)
            .options(selectinload(self.model.participants))
            .filter_by(workspace_id=workspace_id, **filters)
            .order_by(
                getattr(self.model, query.order_by.field).asc()
                if query.order_by.order == 'ASC'
                else getattr(self.model, query.order_by.field).desc()
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

    async def delete_meet(self, meet_id: MeetId) -> None:
        stmt = select(self.model).where(self.model.id == meet_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
