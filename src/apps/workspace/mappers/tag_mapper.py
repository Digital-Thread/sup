from dataclasses import asdict

from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.dtos.tag_dtos import TagOutDTO, UpdateTagAppDTO


class TagMapper:

    @staticmethod
    def entity_to_dto(entity: TagEntity) -> TagOutDTO:
        return TagOutDTO(
            id=entity.id,
            name=entity.name,
            color=entity.color,
        )

    @staticmethod
    def update_data(existing_tag: TagEntity, dto: UpdateTagAppDTO) -> TagEntity:
        for field, value in asdict(dto).items():
            if value is not None and field in ['name', 'color']:
                setattr(existing_tag, field, value)

        return existing_tag
