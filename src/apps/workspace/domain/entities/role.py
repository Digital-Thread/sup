from dataclasses import dataclass, field

from src.apps.workspace.domain.entities.validator_mixins import (
    ColorValidatorMixin,
    NameValidatorMixin,
)
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId


@dataclass
class Role(NameValidatorMixin, ColorValidatorMixin):
    _workspace_id: WorkspaceId
    _name: str
    _color: str
    _id: RoleId | None = field(default=None)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name, 'Роли')
        self._is_valid_color(self._color)

    @property
    def id(self) -> RoleId | None:
        return self._id

    @id.setter
    def id(self, new_id: RoleId) -> None:
        if self._id is not None:
            raise AttributeError('Идентификатор роли уже установлен')

        self._id = new_id

    @property
    def workspace_id(self) -> WorkspaceId:
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
