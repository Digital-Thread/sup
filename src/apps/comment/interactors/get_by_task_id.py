from src.apps.comment.repository import ICommentRepository
from src.apps.comment.dtos import FetchTaskCommentDto, CommentOutDto
from src.apps.comment.domain import TaskId
from src.apps.comment.interactors.base_interactor import BaseInteractor


class GetCommentsByTaskIdInteractor(BaseInteractor):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: FetchTaskCommentDto) -> list[CommentOutDto]:
        comments = await self._repository.get_by_task_id(
            task_id=TaskId(request.task_id),
            page=request.page,
            page_size=request.page_size,
        )
        return comments
