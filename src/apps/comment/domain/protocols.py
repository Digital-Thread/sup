import abc
from typing import Protocol

from .entity import AggregateRoot
from .event import Event


class ICommentRepository[CommentId, Entity: AggregateRoot](Protocol):

    @abc.abstractmethod
    def save(self, entity: Entity) -> Entity | None:
        """
        Сохранить комментарий в базе данных
        :param entity: Сущность комментария для сохранения
        :return: Сохраненная сущность комментария
        """
        pass

    @abc.abstractmethod
    def fetch_by_id(self, comment_id: CommentId) -> Entity | None:
        """
        Получить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: Сущность комментария или None, если комментарий не найден
        """
        pass

    @abc.abstractmethod
    def fetch_all(self) -> list[Entity]:
        """
        Получить список всех комментариев
        :return: Список сущностей комментариев
        """
        pass

    @abc.abstractmethod
    def update_comment(self, comment_id: CommentId, entity: Entity) -> Entity:
        """
        Обновить данные комментария по его ID
        :param comment_id: Идентификатор комментария
        :param entity: Сущность комментария с новыми данными
        :return: Обновленная сущность комментария
        """
        pass

    @abc.abstractmethod
    def delete_comment(self, comment_id: CommentId) -> None:
        """
        Удалить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: None
        """
        pass


class Interactor[Request, Response](Protocol):

    @abc.abstractmethod
    def execute(self, request: Request) -> Response:
        raise NotImplementedError


class IEventHandler(Protocol):
    @abc.abstractmethod
    def handle(self, events: list[Event]) -> None:
        pass
