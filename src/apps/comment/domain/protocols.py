import abc
from typing import Protocol

from .entity import AggregateRoot
from .event import Event


class ICommentRepository[Content, CommentId, Entity: AggregateRoot](Protocol):

    @abc.abstractmethod
    async def save(self, entity: Entity) -> Entity | None:
        """
        Сохранить комментарий в базе данных
        :param entity: Сущность комментария для сохранения
        :return: Сохраненная сущность комментария
        """
        pass

    @abc.abstractmethod
    async def fetch_by_id(self, comment_id: CommentId) -> Entity | None:
        """
        Получить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: Сущность комментария или None, если комментарий не найден
        """
        pass

    @abc.abstractmethod
    async def fetch_all(self, page: int, page_size: int) -> list[Entity]:
        """
        Получить список всех комментариев
        :return: Список сущностей комментариев
        """
        pass

    @abc.abstractmethod
    async def update_comment(self, comment_id: CommentId, new_content: Content) -> Entity:
        """
        Обновить данные комментария по его ID
        :param comment_id: Идентификатор комментария
        :param new_content: Новый комментарий
        :return: Обновленная сущность комментария
        """
        pass

    @abc.abstractmethod
    async def delete_comment(self, comment_id: CommentId) -> None:
        """
        Удалить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: None
        """
        pass


class Interactor[Request, Response](Protocol):

    @abc.abstractmethod
    async def execute(self, request: Request) -> Response:
        raise NotImplementedError


class IEventHandler(Protocol):
    @abc.abstractmethod
    async def handle(self, events: list[Event]) -> None:
        pass
