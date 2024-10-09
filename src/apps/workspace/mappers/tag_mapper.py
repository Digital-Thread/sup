from typing import Any

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagAppDTO, UpdateTagAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class TagMapper(BaseMapper[Tag, TagAppDTO]):
    @staticmethod
    def dto_to_entity(dto: TagAppDTO | UpdateTagAppDTO, immutable_data: dict[str, Any]) -> Tag:

        if isinstance(dto, TagAppDTO):
            tag = Tag(
                _workspace_id=WorkspaceId(dto.workspace_id),
                _name=dto.name,
                _color=dto.color,
                _id=TagId(dto.id),
            )
        else:
            tag = Tag(
                _workspace_id=WorkspaceId(immutable_data.get('workspace_id')),
                _name=dto.get('name'),
                _color=dto.get('color'),
                _id=TagId(immutable_data.get('id')),
            )

        return tag
