from dataclasses import dataclass
from enum import Enum


class UserMeetStatusEnum(str, Enum):
    undefined = 'undefined'
    present = 'present'
    absent = 'absent'
    warned = 'warned'


@dataclass
class InvitedMeetDTO:
    user_id: int
    status: UserMeetStatusEnum = UserMeetStatusEnum.undefined


@dataclass
class ParticipantMeetDTO:
    id: int
    meet_id: int
    user_id: int
    status: UserMeetStatusEnum


@dataclass
class UpdateStatusParticipantMeetDTO:
    user_id: int
    meet_id: int
    status: UserMeetStatusEnum
