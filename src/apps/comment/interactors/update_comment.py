from src.apps.comment import UpdateCommentDto
from src.apps.comment.domain import CommentId
from src.apps.comment.exceptions import CommentNotFoundError, InvalidContentError
from src.apps.comment.interactors.base_interactor import BaseInteractor
from src.apps.comment.repository import ICommentRepository


class UpdateCommentInteractor(BaseInteractor):

    def __init__(
        self,
        comment_repository: ICommentRepository,
    ):
        self._repository = comment_repository

    async def execute(self, request: UpdateCommentDto) -> None:
        comment = await self._repository.get_by_id(comment_id=CommentId(request.comment_id))
        if comment is None:
            raise CommentNotFoundError()

        try:
            comment.update_content(new_content=request.new_content)
        except InvalidContentError as e:
            raise
        await self._repository.update_comment(comment=comment)
