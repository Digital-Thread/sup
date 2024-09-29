from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddMeetDTO:
    name: str
    meet_at: datetime
    category_id: int
    owner_id: int
    assigned_to: int


@dataclass
class MeetDTO(AddMeetDTO):
    id: int
    workspace_id: int
