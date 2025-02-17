from src.apps.comment.domain import CommentId
from src.apps.comment.interactors.base_interactor import Interactor
from src.apps.comment.repository import ICommentRepository
from src.apps.comment.dtos import DeleteCommentDto


class DeleteCommentInteractor(Interactor[DeleteCommentDto, None]):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: DeleteCommentDto) -> None:
        await self._repository.delete_comment(comment_id=CommentId(request.comment_id))
