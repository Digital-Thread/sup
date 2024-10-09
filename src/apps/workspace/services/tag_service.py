from typing import Any, Callable
from uuid import UUID

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.dtos.tag_dtos import TagAppDTO
from src.apps.workspace.repositories.i_tag_repository import ITagRepository
from src.apps.workspace.services.base_service import BaseService


class TagService(BaseService[Tag, TagAppDTO, int, ITagRepository]):
    pass
