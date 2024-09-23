from dataclasses import dataclass
from re import match

from src.apps.workspace.domain.value_objects import RoleID, WorkspaceID


@dataclass
class WorkspaceRole:
    id_: RoleID
    workspace_id: WorkspaceID
    _name: str
    _color: str

    def __post_init__(self) -> None:
        if not self._is_valid_color(self._color):
            raise ValueError(f'Неверный формат цвета {self._color}')
        if not self._is_valid_name(self._name):
            raise ValueError(f'Неверный формат названия роли {self._name}')

    @staticmethod
    def _is_valid_name(name: str) -> bool:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ]+$'
        return bool(match(pattern, name))

    @property
    def name(self) -> str:
        return self._name

    @staticmethod
    def _is_valid_color(color: str) -> bool:
        pattern = r'^#[A-Fa-f0-9]{6}$'
        return bool(match(pattern, color))

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, new_color: str) -> None:
        if not self._is_valid_color(new_color):
            raise ValueError(f'Неверный формат цвета {new_color}')

        self._color = new_color
