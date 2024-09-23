from dataclasses import (
    dataclass,
    field,
)
from typing import List

from src.apps.workspace.domain.value_objects import (
    CategoryID,
    WorkspaceID,
)


@dataclass
class WorkspaceCategory:
    id_: CategoryID
    name: str
    _workspace_ids: List[WorkspaceID] = field(default_factory=list)

    @staticmethod
    def _validate_workspace_id(workspace_id: WorkspaceID) -> bool:
        if workspace_id >= 0:
            return True

    @property
    def workspaces(self):
        return self._workspace_ids

    @workspaces.setter
    def workspaces(self, workspace_id: WorkspaceID) -> None:
        if self._validate_workspace_id(workspace_id):
            self._workspace_ids.append(workspace_id)
