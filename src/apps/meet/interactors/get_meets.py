from ..dtos import MeetOutputDTO
from ..mappers import MeetMapper
from ..query_parameters import MeetListQuery
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class GetListMeetsInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository):
        self._repository = meet_repository

    async def execute(self, query: MeetListQuery) -> list[MeetOutputDTO] | None:
        meet = await self._repository.get_all(query)
        return [MeetMapper.entity_to_dto(m) for m in meet] if meet else None
