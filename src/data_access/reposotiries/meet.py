from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.meet.entities.participant_dtos import (
    InvitedMeetDTO,
    ParticipantMeetDTO,
    UpdateStatusParticipantMeetDTO,
)
from src.apps.meet.entities.meet_dtos import AddMeetDTO, MeetDTO
from src.apps.meet.repositories import (
    IMeetRepository,
    IMeetRepositoryFactory,
    IParticipantRepository,
)
from src.data_access.models import Meet


class RepositoryFactory(IMeetRepositoryFactory):
    def __init__(self, workspace_id: int, session: AsyncSession):
        self.workspace_id = workspace_id
        self._session = session

    def get_meet_repository(self) -> IMeetRepository:
        return MeetRepository(self.workspace_id, self._session)

    def get_participant_repository(self) -> IParticipantRepository:
        return ParticipantRepository(self.workspace_id, self._session)


class MeetRepository(IMeetRepository):
    def __init__(self, workspace_id: int, session: AsyncSession):
        self.workspace_id = workspace_id
        self._session = session

    async def get_meets(self) -> list[MeetDTO]:
        query = select(Meet)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_meet_by_id(self, id_: int) -> MeetDTO:
        query = select(Meet).where(Meet.id == id_)
        result = await self._session.execute(query)
        meet = result.scalar_one_or_none()
        if not meet:
            raise Exception('Meet not found')
        return meet

    async def add_meet(self, dto: AddMeetDTO) -> None:
        new_meet = Meet(**dto.dict())
        self._session.add(new_meet)
        await self._session.commit()


class ParticipantRepository(IParticipantRepository):
    def __init__(self, workspace_id: int, session: AsyncSession):
        self.workspace_id = workspace_id
        self._session = session

    async def get_participants_by_meet_id(self, meet_id: int) -> list[ParticipantMeetDTO]:
        query = select(Meet).where(Meet.id == meet_id)
        result = await self._session.execute(query)
        meet = result.scalar_one_or_none()
        if not meet:
            raise Exception('Meet not found')
        return meet.participants

    async def invite(self, meet_id: int, dto: InvitedMeetDTO) -> None:
        query = select(Meet).where(Meet.id == meet_id)
        result = await self._session.execute(query)
        meet = result.scalar_one_or_none()
        if not meet:
            raise Exception('Meet not found')
        meet.participants.append(ParticipantMeetDTO(**dto.dict()))
        await self._session.commit()

    async def check_participant(self, meet_id: int, dto: UpdateStatusParticipantMeetDTO) -> None:
        query = select(Meet).where(Meet.id == meet_id)
        result = await self._session.execute(query)
        meet = result.scalar_one_or_none()
        if not meet:
            raise Exception('Meet not found')
        if dto.status == 'accepted':
            meet.participants.append(ParticipantMeetDTO(**dto.dict()))
        elif dto.status == 'declined':
            meet.participants.remove(ParticipantMeetDTO(**dto.dict()))
        await self._session.commit()
