from dataclasses import dataclass, field
from typing import Set

from src.apps.workspace.domain.value_objects import CategoryID, WorkspaceID


@dataclass
class WorkspaceCategory:
    id_: CategoryID
    name: str
    _workspace_ids: Set[WorkspaceID] = field(default_factory=set)

    @staticmethod
    def _validate_workspace_id(workspace_id: WorkspaceID) -> bool:
        return workspace_id >= 0

    @property
    def workspaces(self) -> Set[WorkspaceID]:
        return self._workspace_ids

    @workspaces.setter
    def workspaces(self, workspace_id: WorkspaceID) -> None:
        if self._validate_workspace_id(workspace_id):
            self._workspace_ids.add(workspace_id)
