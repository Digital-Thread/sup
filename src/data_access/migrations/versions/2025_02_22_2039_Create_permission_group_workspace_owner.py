from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'b3f7a9c1d682'
down_revision = 'a0d9800b2b0c'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # Получаем ID разрешений по их code
    permission_codes = [
        'workspace.read', 'workspace.delete', 'workspace.read_members', 'workspace.update',
        'role.create', 'role.read', 'role.read_all', 'role.update', 'role.delete',
        'role.assign_to_member', 'role.remove_from_member', 'tag.create', 'tag.read', 'tag.read_all',
        'tag.update', 'tag.delete', 'category.create', 'category.read', 'category.read_all',
        'category.update', 'category.delete', 'w_invite.create', 'w_invite.read_all', 'w_invite.update',
        'w_invite.delete', 'comment.create', 'comment.read_all', 'comment.update', 'comment.delete',
        'project.create', 'project.read', 'project.read_all', 'project.update', 'project.delete',
        'feature.create', 'feature.read', 'feature.read_all', 'feature.update', 'feature.delete',
        'task.create', 'task.read', 'task.read_all', 'task.update', 'task.delete', 'meet.create',
        'meet.read', 'meet.read_all', 'meet.update', 'meet.delete', 'meet.update_participants',
        'perm_group.create', 'perm_group.read', 'perm_group.read_all', 'perm_group.update', 'perm_group.delete'
    ]

    permission_query = sa.text("""
        SELECT id FROM permissions WHERE code = ANY(:permission_codes)
    """)
    permission_ids = [row[0] for row in connection.execute(permission_query, {'permission_codes': permission_codes})]

    # Создаем новую группу разрешений
    group_insert = sa.text("""
        INSERT INTO permission_groups (is_global, workspace_id, name, description)
        VALUES (:is_global, :workspace_id, :name, :description)
        RETURNING id
    """)
    group_id = connection.execute(group_insert, {
        'is_global': True,
        'workspace_id': None,
        'name': 'Workspace_owner',
        'description': 'Permissions granting full control to workspace owners'
    }).fetchone()[0]

    # Добавляем разрешения в группу
    permission_insert = sa.text("""
        INSERT INTO permission_group_permissions (permission_group_id, permission_id)
        VALUES (:group_id, :permission_id)
    """)
    for permission_id in permission_ids:
        connection.execute(permission_insert, {'group_id': group_id, 'permission_id': permission_id})


def downgrade():
    connection = op.get_bind()

    # Удаляем группу разрешений
    group_id_query = sa.text("""
        SELECT id FROM permission_groups WHERE name = 'Workspace_owner'
    """)
    group_id = connection.execute(group_id_query).fetchone()

    if group_id:
        group_id = group_id[0]
        op.execute("DELETE FROM permission_group_permissions WHERE permission_group_id = :group_id",
                   {'group_id': group_id})
        op.execute("DELETE FROM permission_groups WHERE id = :group_id", {'group_id': group_id})
