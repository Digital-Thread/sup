from uuid import UUID


class WorkspaceContext:
    def __init__(self, workspace_id: UUID | None) -> None:
        self.workspace_id = workspace_id
