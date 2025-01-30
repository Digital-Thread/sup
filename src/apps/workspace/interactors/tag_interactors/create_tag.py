from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.tag_dtos import CreateTagDTO
from src.apps.workspace.exceptions.tag_exceptions import (
    TagAlreadyExists,
    TagException,
    WorkspaceTagNotFound,
)
from src.apps.workspace.repositories.tag_repository import ITagRepository


class CreateTagInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, create_tag_data: CreateTagDTO) -> None:
        try:
            await self._tag_repository.save(
                TagEntity(
                    _name=create_tag_data.name,
                    _color=create_tag_data.color,
                    _workspace_id=WorkspaceId(create_tag_data.workspace_id),
                )
            )
        except (ValueError, WorkspaceTagNotFound, TagAlreadyExists) as error:
            raise TagException(f'{str(error)}')
