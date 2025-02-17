import abc
from typing import Protocol


class Interactor[Request, Response](Protocol):

    @abc.abstractmethod
    async def execute(self, request: Request) -> Response:
        raise NotImplementedError
