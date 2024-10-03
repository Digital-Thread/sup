from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.exceptions.tag_exceptions import TagAlreadyExists
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class CreateTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag: Tag) -> None:
        try:
            await self._tag_repository.save(tag)
        except TagAlreadyExists:
            raise ValueError(f'Тег {tag.name} уже существует')
