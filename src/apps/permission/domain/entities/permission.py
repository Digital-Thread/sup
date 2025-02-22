from src.apps.permission.domain.types_ids import PermissionId


class PermissionEntity:

    def __init__(
            self,
            code: str,
            description: str,
            is_hidden: bool = False
    ) -> None:
        self._id: PermissionId | None = None
        self.code = code
        self.description = description
        self.is_hidden = is_hidden
