from abc import ABC, abstractmethod
from typing import Any


class BaseInteractor(ABC):

    @abstractmethod
    async def execute(self, *args: Any) -> Any:
        raise NotImplementedError
