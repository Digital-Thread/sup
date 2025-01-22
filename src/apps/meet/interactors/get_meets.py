from ..dtos import MeetOutputDTO
from ..mappers import MeetMapper
from ..query_parameters import MeetListQuery
from ..repositories import IMeetRepository
from .base_interactor import BaseInteractor


class GetListMeetsInteractor(BaseInteractor):
    def __init__(self, meet_repository: IMeetRepository, query: MeetListQuery):
        self._repository = meet_repository
        self._query = query

    async def execute(self) -> list[MeetOutputDTO] | None:
        meet = await self._repository.get_list(self._query)
        return [MeetMapper.entity_to_dto(m) for m in meet] if meet else None
