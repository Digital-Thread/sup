from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.meet.entities.meet_dtos import AddMeetDTO, MeetDTO
from src.apps.meet.repositories import IMeetRepository
from src.data_access.models import Meet


class MeetRepository(IMeetRepository):
    def __init__(self, session: AsyncSession):
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
