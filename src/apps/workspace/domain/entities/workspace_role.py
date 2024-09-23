from re import match
from dataclasses import dataclass

from src.apps.workspace.domain.value_objects import (
    RoleID,
    WorkspaceID,
)


@dataclass
class WorkspaceRole:
    id_: RoleID
    workspace_id: WorkspaceID
    name: str
    _color: str

    @staticmethod
    def _validate_color(color: str) -> bool:
        pattern = r'^#[A-Fa-f0-9]{6}$'
        return bool(match(pattern, color))

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, new_color: str) -> None:
       if self._validate_color(new_color):
           self._color = new_color
