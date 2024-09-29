from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.apps.workspace.domain.entities.validator_mixins import NameValidatorMixin


@dataclass
class Category(NameValidatorMixin):
    _name: str
    id: Optional[int] = field(default=None)
    workspace_ids: set[UUID] = field(default_factory=set)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name, 'Категории')

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._is_valid_name(new_name, 'Категории')
        self._name = new_name
