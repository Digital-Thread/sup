from src.apps.comment.domain import (
    AuthorId,
    CommentEntity,
    CommentId,
    Content,
    FeatureId,
    TaskId,
)
from src.data_access.models import CommentModel


class CommentMapper:
    @staticmethod
    def convert_comment_entity_to_db_model(comment: CommentEntity) -> CommentModel:
        if comment.comment_id is None:
            return CommentModel(
                user_id=comment.user_id.to_raw(),
                task_id=getattr(comment.task_id, 'to_raw', lambda: None)(),
                feature_id=getattr(comment.feature_id, 'to_raw', lambda: None)(),
                content=comment.content.to_raw(),
                created_at=comment.created_at,
                updated_at=comment.updated_at,
            )
        else:
            return CommentModel(
                id=comment.comment_id.to_raw(),
                user_id=comment.user_id.to_raw(),
                task_id=getattr(comment.task_id, 'to_raw', lambda: None)(),
                feature_id=getattr(comment.feature_id, 'to_raw', lambda: None)(),
                content=comment.content.to_raw(),
                created_at=comment.created_at,
                updated_at=comment.updated_at,
            )

    @staticmethod
    def convert_db_model_to_comment_entity(comment: CommentModel) -> CommentEntity:
        return CommentEntity(
            comment_id=CommentId(comment.id),
            user_id=AuthorId(comment.user_id),  # type: ignore
            task_id=TaskId(comment.task_id) if comment.task_id else None,
            feature_id=FeatureId(comment.feature_id) if comment.feature_id else None,
            content=Content(comment.content),
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
