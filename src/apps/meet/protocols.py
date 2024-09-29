from typing import Protocol


class UserServiceProtocol(Protocol):
    def get_user_by_id(self, user_id: int):
        pass


class WorkspaceServiceProtocol(Protocol):
    def get_workspace_by_id(self, workspace_id: int):
        pass
