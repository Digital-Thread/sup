from src.apps.comment.domain import AuthorId, FeatureId, TaskId
from src.apps.comment.domain.comment import CommentEntity
from src.apps.comment.dtos import BaseCommentDto


class CommentMapper:
    @staticmethod
    def dto_to_entity(dto: BaseCommentDto) -> CommentEntity:
        return CommentEntity(
            user_id=AuthorId(dto.user_id),
            task_id=TaskId(dto.task_id) if dto.task_id is not None else None,
            feature_id=FeatureId(dto.feature_id) if dto.feature_id is not None else None,
            content=dto.content,
        )
