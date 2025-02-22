class PermissionMixin:
    required_permission: str = None  # Переопределяется в конкретных интеракторах

    def check_permissions(self) -> None:
        if self.required_permission is not None:
            pass

    async def execute(self) -> any:
        self.check_permissions()
        return await super().execute()
