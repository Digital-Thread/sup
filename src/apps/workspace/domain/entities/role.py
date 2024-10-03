from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.apps.workspace.domain.entities.validator_mixins import (
    ColorValidatorMixin,
    NameValidatorMixin,
)


@dataclass
class Role(NameValidatorMixin, ColorValidatorMixin):
    _workspace_id: UUID
    _name: str
    _color: str
    id: Optional[int] = field(default=None)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name, 'Роли')
        self._is_valid_color(self._color)

    @property
    def workspace_id(self) -> UUID:
        return self._workspace_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._is_valid_name(new_name, 'Роли')
        self._name = new_name

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, new_color: str) -> None:
        self._is_valid_color(new_color)
        self._color = new_color
