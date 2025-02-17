from abc import ABC, abstractmethod

from src.apps.comment.domain import (
    CommentEntity,
    CommentId,
    TaskId,
    FeatureId,
)


class ICommentRepository(ABC):

    @abstractmethod
    async def save(self, entity: CommentEntity) -> None:
        """
        Сохранить комментарий в базе данных
        :param entity: Сущность комментария для сохранения
        :return: None
        """
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: CommentId) -> CommentEntity | None:
        """
        Получить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: Сущность комментария или None, если комментарий не найден
        """
        pass


    @abstractmethod
    async def update_comment(self, comment: CommentEntity) -> None:
        """
        Обновить данные комментария по его ID
        :param comment: Сущность комментария с новым контентом
        :return: None
        """
        pass

    @abstractmethod
    async def delete_comment(self, comment_id: CommentId) -> None:
        """
        Удалить комментарий по его ID
        :param comment_id: Идентификатор комментария
        :return: None
        """
        pass

    @abstractmethod
    async def get_by_task_id(
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

    @abstractmethod
    async def get_by_feature_id(
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
