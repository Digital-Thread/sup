from src.apps.workspace.exceptions.tag_exceptions import TagNotFound
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class DeleteTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: int) -> None:
        try:
            await self._tag_repository.delete(tag_id)
        except TagNotFound:
            ValueError(f'Тег с id={tag_id} не существует')
