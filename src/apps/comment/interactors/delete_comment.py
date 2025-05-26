from src.apps.comment.domain import CommentId
from src.apps.comment.dtos import DeleteCommentDto
from src.apps.comment.exceptions import CommentNotFoundError, CommentRepositoryError
from src.apps.comment.interactors.base_interactor import BaseInteractor
from src.apps.comment.repository import ICommentRepository


class DeleteCommentInteractor(BaseInteractor):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: DeleteCommentDto) -> None:
        try:
            await self._repository.delete_comment(comment_id=CommentId(request.comment_id))
        except CommentRepositoryError as e:
            raise CommentNotFoundError()
