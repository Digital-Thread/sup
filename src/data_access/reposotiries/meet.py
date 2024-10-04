from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.meet.entities.meet import Meet
from src.apps.meet.entities.participant import Participant
from src.apps.meet.entities.value_objects import MeetId, ParticipantId
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

    async def create_meet(self, meet: Meet) -> MeetId | None:
        try:
            smtp = insert(self.model).values(**meet.__dict__).returning(self.model.id)
            result = await self._session.execute(smtp)
            await self._session.commit()
            return MeetId(result.scalar_one()) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_meets(self, workspace_id: int, query: MeetListQuery) -> list[Meet] | None:
        smtp = (
            select(self.model)
            .filter_by(workspace_id=workspace_id, **query.filters.__dict__)
            .order_by(
                getattr(self.model, query.order_by.field.value).asc()
                if query.order_by.order == SortOrder.ASC
                else getattr(self.model, query.order_by.field.value).desc()
            )
            .limit(query.limit)
            .offset(query.offset)
        )
        result = await self._session.execute(smtp)
        if not result:
            return None
        data = result.mappings().all()
        return [Meet(**d) for d in data]

    async def get_meet_by_id(self, meet_id: MeetId) -> Meet | None:
        smtp = select(self.model).where(self.model.id == meet_id)
        result = await self._session.execute(smtp)
        meet = result.mappings().one_or_none()
        if not meet:
            return None
        return Meet(**meet)

    async def update_meet(self, meet: Meet) -> MeetId | None:
        try:
            smtp = (
                update(self.model)
                .where(self.model.id == meet.id)
                .values(**meet.__dict__)
                .returning(self.model)
            )
            result = await self._session.execute(smtp)
            await self._session.commit()
            return MeetId(result.scalar_one().id) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e


class ParticipantRepository(IParticipantRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = ParticipantModel

    async def get_participants_by_meet_id(self, meet_id: MeetId) -> list[Participant] | None:
        smtp = select(self.model).where(self.model.meet_id == meet_id)
        result = await self._session.execute(smtp)
        data = result.mappings().all()
        if not data:
            return None
        return [Participant(**d) for d in data]

    async def invite(self, participant: Participant) -> ParticipantId | None:
        try:
            smtp = insert(self.model).values(**participant.__dict__).returning(self.model.id)
            result = await self._session.execute(smtp)
            await self._session.commit()
            return ParticipantId(result.scalar_one()) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def update_participant(self, participant: Participant) -> ParticipantId | None:
        try:
            smtp = (
                update(self.model)
                .where(self.model.id == participant.id)
                .values(**participant.__dict__)
                .returning(self.model)
            )
            result = await self._session.execute(smtp)
            await self._session.commit()
            return ParticipantId(result.scalar_one().id) if result else None
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e
