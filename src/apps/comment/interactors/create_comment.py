from src.apps.comment.exceptions import BaseCommentException, CommentRepositoryError
from src.apps.comment import AddCommentDto
from src.apps.comment.mapper import CommentMapper
from src.apps.comment.interactors.base_interactor import BaseInteractor
from src.apps.comment.repository import ICommentRepository


class CreateCommentInteractor(BaseInteractor):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: AddCommentDto) -> None:
        try:
            comment_entity = CommentMapper.dto_to_entity(request)
        except BaseCommentException as e:
            raise

        try:
            await self._repository.save(comment_entity)
        except CommentRepositoryError as e:
            raise
