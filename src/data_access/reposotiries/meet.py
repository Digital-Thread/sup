from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.meet.dtos import MeetInputDTO, MeetResponseDTO
from apps.meet.entities.participant_dtos import (
    InvitedMeetDTO,
    ParticipantMeetDTO,
)
from data_access.models.meet import Participant
from src.apps.meet.repositories import (
    IMeetRepository,
    IParticipantRepository,
)
from src.apps.meet.temp_dtos import UserInputDTO, WorkspaceInputDTO
from src.data_access.models import Meet


class MeetRepository(IMeetRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_meets(
        self, workspace: WorkspaceInputDTO, owner: UserInputDTO, **filter_by: str | int
    ) -> list[MeetResponseDTO] | None:
        query = (
            select(Meet)
            .where(and_(Meet.workspace_id == workspace.id, Meet.owner_id == owner.id))
            .filter_by(**filter_by)
        )
        result = await self._session.execute(query)
        if not result:
            return None
        data = result.mappings().all()
        return [MeetResponseDTO(**d) for d in data]

    async def get_meet_by_id(self, id_: int) -> MeetResponseDTO | None:
        query = select(Meet).where(Meet.id == id_)
        result = await self._session.execute(query)
        meet = result.mappings().one_or_none()
        if not meet:
            return None
        return MeetResponseDTO(**meet)

    async def add_meet(self, dto: MeetInputDTO) -> int:
        try:
            query = insert(Meet).values(**dto.__dict__).returning(Meet.id)
            result = await self._session.execute(query)
            await self._session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e


class ParticipantRepository(IParticipantRepository):
    def __init__(self, workspace_id: int, session: AsyncSession):
        self.workspace_id = workspace_id
        self._session = session

    async def get_participants_by_meet_id(self, meet_id: int) -> list[ParticipantMeetDTO] | None:
        query = select(Participant).where(Meet.id == meet_id)
        result = await self._session.execute(query)
        data = result.mappings().all()
        if not data:
            return None
        return [ParticipantMeetDTO(**d) for d in data]

    async def invite(self, meet_id: int, dto: InvitedMeetDTO) -> MeetResponseDTO | None:
        query = select(Meet).where(Meet.id == meet_id)
        result = await self._session.execute(query)
        meet = result.mappings().one_or_none()
        if not meet:
            return None
        return MeetResponseDTO(**meet)

    async def add_meet(self, dto: MeetInputDTO) -> int:
        try:
            query = insert(Meet).values(**dto.__dict__).returning(Meet.id)
            result = await self._session.execute(query)
            await self._session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e
