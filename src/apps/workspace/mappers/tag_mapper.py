from typing import Any

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagAppDTO, UpdateTagAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class TagMapper(BaseMapper[Tag, TagAppDTO]):

    @staticmethod
    def dto_to_entity(dto: TagAppDTO) -> Tag:

        return Tag(
            _workspace_id=WorkspaceId(dto.workspace_id),
            _name=dto.name,
            _color=dto.color,
            _id=TagId(dto.id),
        )

    @staticmethod
    def update_data(existing_tag: Tag, dto: UpdateTagAppDTO) -> Tag:
        for field, value in dto.items():
            if value is not None:
                setattr(existing_tag, field, value)

        return existing_tag
