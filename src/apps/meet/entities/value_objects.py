from typing import NewType
from uuid import UUID

MeetId = NewType('MeetId', int)
ParticipantId = NewType('ParticipantId', int)
WorkspaceId = NewType('WorkspaceId', int)
OwnerId = NewType('OwnerId', UUID)
AssignedId = NewType('AssignedId', UUID)
CategoryId = NewType('CategoryId', int)
UserId = NewType('UserId', UUID)
