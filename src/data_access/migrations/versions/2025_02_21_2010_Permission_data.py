from alembic import op
import sqlalchemy as sa

revision = "6cf92e7445ab"
down_revision = "5ba81d9880ff"
branch_labels = None
depends_on = None


def upgrade():
    permissions = [
        {"code": "workspace.create", "description": "Создание рабочего пространства", "is_hidden": True},
        {"code": "workspace.read", "description": "Просмотр рабочего пространства", "is_hidden": True},
        {"code": "workspace.read_own", "description": "Просмотр своих рабочих пространств", "is_hidden": True},
        {"code": "workspace.delete", "description": "Удаление рабочего пространства", "is_hidden": True},
        {"code": "workspace.read_members", "description": "Просмотр участников рабочего пространства", "is_hidden": False},
        {"code": "workspace.update", "description": "Обновление рабочего пространства", "is_hidden": False},

        {"code": "role.create", "description": "Создание роли", "is_hidden": False},
        {"code": "role.read", "description": "Просмотр роли", "is_hidden": False},
        {"code": "role.read_all", "description": "Просмотр всех ролей", "is_hidden": False},
        {"code": "role.update", "description": "Обновление роли", "is_hidden": False},
        {"code": "role.delete", "description": "Удаление роли", "is_hidden": False},
        {"code": "role.assign_to_member", "description": "Назначение ролей участникам", "is_hidden": False},
        {"code": "role.remove_from_member", "description": "Удаление ролей у участников", "is_hidden": False},

        {"code": "tag.create", "description": "Создание тега", "is_hidden": False},
        {"code": "tag.read", "description": "Просмотр тега", "is_hidden": False},
        {"code": "tag.read_all", "description": "Просмотр всех тегов", "is_hidden": False},
        {"code": "tag.update", "description": "Обновление тега", "is_hidden": False},
        {"code": "tag.delete", "description": "Удаление тега", "is_hidden": False},

        {"code": "category.create", "description": "Создание категории", "is_hidden": False},
        {"code": "category.read", "description": "Просмотр категории", "is_hidden": False},
        {"code": "category.read_all", "description": "Просмотр всех категорий", "is_hidden": False},
        {"code": "category.update", "description": "Обновление категории", "is_hidden": False},
        {"code": "category.delete", "description": "Удаление категории", "is_hidden": False},

        {"code": "w_invite.create", "description": "Создание приглашения в рабочее пространство", "is_hidden": False},
        {"code": "w_invite.read_all", "description": "Просмотр всех приглашений в рабочее пространство", "is_hidden": False},
        {"code": "w_invite.update", "description": "Обновление статуса приглашения", "is_hidden": False},
        {"code": "w_invite.delete", "description": "Удаление приглашения в рабочее пространство", "is_hidden": False},

        {"code": "comment.create", "description": "Создание комментария", "is_hidden": False},
        {"code": "comment.read_all", "description": "Просмотр всех комментариев", "is_hidden": False},
        {"code": "comment.update", "description": "Обновление комментария", "is_hidden": False},
        {"code": "comment.delete", "description": "Удаление комментария", "is_hidden": False},

        {"code": "project.create", "description": "Создание проекта", "is_hidden": False},
        {"code": "project.read", "description": "Просмотр проекта", "is_hidden": False},
        {"code": "project.read_all", "description": "Просмотр всех проектов", "is_hidden": False},
        {"code": "project.update", "description": "Обновление проекта", "is_hidden": False},
        {"code": "project.delete", "description": "Удаление проекта", "is_hidden": False},

        {"code": "feature.create", "description": "Создание фичи", "is_hidden": False},
        {"code": "feature.read", "description": "Просмотр фичи", "is_hidden": False},
        {"code": "feature.read_all", "description": "Просмотр всех фичей", "is_hidden": False},
        {"code": "feature.update", "description": "Обновление фичи", "is_hidden": False},
        {"code": "feature.delete", "description": "Удаление фичи", "is_hidden": False},

        {"code": "task.create", "description": "Создание задачи", "is_hidden": False},
        {"code": "task.read", "description": "Просмотр задачи", "is_hidden": False},
        {"code": "task.read_all", "description": "Просмотр всех задач", "is_hidden": False},
        {"code": "task.update", "description": "Обновление задачи", "is_hidden": False},
        {"code": "task.delete", "description": "Удаление задачи", "is_hidden": False},

        {"code": "meet.create", "description": "Создание встречи", "is_hidden": False},
        {"code": "meet.read", "description": "Просмотр встречи", "is_hidden": False},
        {"code": "meet.read_all", "description": "Просмотр всех встреч", "is_hidden": False},
        {"code": "meet.update", "description": "Обновление встречи", "is_hidden": False},
        {"code": "meet.delete", "description": "Удаление встречи", "is_hidden": False},
        {"code": "meet.update_participants", "description": "Обновить список участников встречи", "is_hidden": False},

        {"code": "perm_group.create", "description": "Создание группы прав", "is_hidden": False},
        {"code": "perm_group.read", "description": "Просмотр группы прав", "is_hidden": False},
        {"code": "perm_group.read_all", "description": "Просмотр всех групп прав", "is_hidden": False},
        {"code": "perm_group.update", "description": "Обновление группы прав", "is_hidden": False},
        {"code": "perm_group.delete", "description": "Удаление группы прав", "is_hidden": False}
    ]

    op.bulk_insert(
        sa.table(
            "permissions",
            sa.column("code", sa.String),
            sa.column("description", sa.String),
            sa.column("is_hidden", sa.Boolean),
        ),
        permissions,
    )


def downgrade():
    op.execute("""
        DELETE FROM permissions WHERE code LIKE 'workspace.%' OR code LIKE 'role.%' OR code LIKE 'tag.%' 
        OR code LIKE 'category.%' OR code LIKE 'w_invite.%' OR code LIKE 'comment.%' OR code LIKE 'project.%'
        OR code LIKE 'feature.%' OR code LIKE 'task.%' OR code LIKE 'meet.%' OR code LIKE 'perm_group.%'
    """)
