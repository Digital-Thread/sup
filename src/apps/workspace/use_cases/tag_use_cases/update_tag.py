from src.apps.workspace.domain.types_ids import TagId
from src.apps.workspace.dtos.tag_dtos import UpdateTagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import TagNotFound, TagNotUpdated
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class UpdateTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    async def execute(self, tag_id: TagId, update_data: UpdateTagAppDTO) -> None:
        try:
            existing_tag = await self.tag_repository.find_by_id(tag_id)
        except TagNotFound:
            pass
            # TODO пробросить дальше
        else:
            updated_tag = TagMapper.update_data(existing_tag, update_data)

            try:
                await self.tag_repository.update(updated_tag)
            except TagNotUpdated:
                pass
                # TODO пробросить дальше
