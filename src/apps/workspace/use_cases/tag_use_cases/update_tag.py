from src.apps.workspace.dtos.tag_dtos import UpdateTagAppDTO
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class UpdateTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    async def execute(self, tag_id: int, update_data: UpdateTagAppDTO) -> None:
        """
        Используем метод с полной загрузкой объекта из БД, т.к. есть поля с валидацией
        """
        tag = await self.tag_repository.find_by_id(tag_id)

        if update_data.get('name'):
            tag.name = update_data['name']

        if update_data.get('color'):
            tag.color = update_data['color']

        await self.tag_repository.update(tag)
