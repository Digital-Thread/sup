from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.apps.workspace.domain.entities.validator_mixins import (
    ColorValidatorMixin,
    NameValidatorMixin,
)
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId


@dataclass
class Tag(NameValidatorMixin, ColorValidatorMixin):
    _workspace_id: WorkspaceId
    _name: str
    _color: str
    _id: Optional[TagId] = field(default=None)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name, 'Тега')
        self._is_valid_color(self._color)

    @property
    def id(self) -> Optional[TagId]:
        return self._id

    @property
    def workspace_id(self) -> WorkspaceId:
        return self._workspace_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._is_valid_name(new_name, 'Тега')
        self._name = new_name

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, new_color: str) -> None:
        self._is_valid_color(new_color)
        self._color = new_color
