import abc
from typing import Protocol

from .comment import CommentEntity
from .event import Event
from .types_ids import CommentId, Content, FeatureId, TaskId


class ICommentRepository(Protocol):

    @abc.abstractmethod
    async def save(self, entity: CommentEntity) -> CommentEntity | None:
        """
        Сохранить комментарий в базе данных
        :param entity: Сущность комментария для сохранения
        :return: Сохраненная сущность комментария
        """
        pass

    @abc.abstractmethod
    async def fetch_by_id(self, comment_id: CommentId) -> CommentEntity | None:
        """
        Получить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: Сущность комментария или None, если комментарий не найден
        """
        pass

    @abc.abstractmethod
    async def fetch_all(self, page: int, page_size: int) -> list[CommentEntity]:
        """
        Получить список всех комментариев
        :return: Список сущностей комментариев
        """
        pass

    @abc.abstractmethod
    async def update_comment(self, comment_id: CommentId, new_content: Content) -> CommentEntity:
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

    @abc.abstractmethod
    async def fetch_task_comments(
        self, task_id: TaskId, page: int, page_size: int
    ) -> list[CommentEntity]:
        """
        Получить список комментариев для задачи
        :param task_id: Идентификатор задачи
        :param page: Номер страницы
        :param page_size: Размер страницы
        :return: Список сущностей комментариев
        """
        pass

    @abc.abstractmethod
    async def fetch_feature_comments(
        self, feature_id: FeatureId, page: int, page_size: int
    ) -> list[CommentEntity]:
        """
        Получить список комментариев для фичи
        :param feature_id: Идентификатор фичи
        :param page: Номер страницы
        :param page_size: Размер страницы
        :return: Список сущностей комментариев
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
