from datetime import datetime


class Meet:
    def __init__(
        self,
        name: str,
        meet_at: datetime,
        category_id: int,
        owner_id: int,
        assigned_to: int,
    ):
        self.name = name
        self.meet_at = meet_at
        self.category_id = category_id
        self.owner_id = owner_id
        self.assigned_to = assigned_to

    @property
    def meet_at(self) -> datetime:
        return self._meet_at

    @meet_at.setter
    def meet_at(self, value: datetime):
        if value is not None:
            value = value.replace(tzinfo=None)
        self._meet_at = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def category_id(self) -> int:
        return self._category_id

    @category_id.setter
    def category_id(self, value: int):
        self._category_id = value

    @property
    def owner_id(self) -> int:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: int):
        self._owner_id = value

    @property
    def assigned_to(self) -> int:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: int):
        self._assigned_to = value

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def workspace_id(self) -> int:
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, value: int):
        self._workspace_id = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime):
        self._created_at = value

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: datetime):
        self._updated_at = value
