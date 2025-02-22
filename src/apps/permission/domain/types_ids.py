from typing import NewType
from uuid import UUID

PermissionId = NewType('PermissionId', int)
PermissionCode = NewType('PermissionCode', str)
PermissionGroupId = NewType('PermissionGroupId', int)
WorkspaceId = NewType('WorkspaceId', UUID)
UserId = NewType('UserId', UUID)
