from collections.abc import Callable
from typing import Any, Mapping
from uuid import UUID


class BaseService[T, ID, R]:
    """
    Базовый сервис для работы с сущностями.

    Параметры:
    T: Тип сущности, который будет обрабатываться этим сервисом.
    ID: Тип идентификатора сущности (int или UUID).
    R: Тип репозитория, который будет использоваться для доступа к данным.
    """

    def __init__(self, repository: R):
        self._repository = repository

    async def _execute_use_case(self, use_case: Callable[[R], Any], *args: Any) -> Any:
        """Вспомогательный метод для вызова use_case с репозиторием и аргументами."""
        use_case_instance = use_case(self._repository)
        return await use_case_instance.execute(*args)

    async def create(self, entity: T, use_case: Callable[[R], Any]) -> None:
        await self._execute_use_case(use_case, entity)

    async def retrieve_by_id(self, entity_id: ID, use_case: Callable[[R], Any]) -> T:
        return await self._execute_use_case(use_case, entity_id)

    async def update(
        self, entity_id: ID, update_data: Mapping[str, Any], use_case: Callable[[R], Any]
    ) -> None:
        await self._execute_use_case(use_case, entity_id, update_data)

    async def delete(self, entity_id: ID, use_case: Callable[[R], Any]) -> None:
        await self._execute_use_case(use_case, entity_id)

    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[R], Any]
    ) -> list[T]:
        """Общий метод для получения сущностей по ID рабочего пространства."""
        return await self._execute_use_case(use_case, workspace_id)
