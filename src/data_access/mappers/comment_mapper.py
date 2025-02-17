from src.apps.comment.domain import (
    AuthorId,
    CommentEntity,
    CommentId,
    FeatureId,
    TaskId,
)
from src.data_access.models import CommentModel


class CommentMapper:
    @staticmethod
    def convert_comment_entity_to_db_model(entity: CommentEntity) -> CommentModel:
        if entity.id is None:
            return CommentModel(
                user_id=entity.user_id,
                task_id=entity.task_id,
                feature_id=entity.feature_id,
                content=entity.content,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
        else:
            return CommentModel(
                id=entity.id,
                user_id=entity.user_id,
                task_id=entity.task_id,
                feature_id=entity.feature_id,
                content=entity.content,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )

    @staticmethod
    def convert_db_model_to_comment_entity(model: CommentModel) -> CommentEntity:
        comment = CommentEntity(
            user_id=AuthorId(model.user_id),  # type: ignore
            task_id=TaskId(model.task_id) if model.task_id else None,
            feature_id=FeatureId(model.feature_id) if model.feature_id else None,
            content=model.content,
        )
        comment.id = CommentId(model.id)
        comment.created_at = model.created_at
        comment.updated_at = model.updated_at
        return comment
