from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import (
    InviteId,
    MeetId,
    MemberId,
    OwnerId,
    ProjectId,
    RoleId,
    TagId,
    WorkspaceId,
)
from tests.fixtures.workspace_fixtures import owner_id, two_member_ids, workspace_id


@pytest.fixture()
def workspace_minimal(owner_id: OwnerId) -> Workspace:
    return Workspace(owner_id=owner_id, _name='Minimal Workspace')


@pytest.fixture()
def workspace_full(
    owner_id: OwnerId, workspace_id: WorkspaceId, two_member_ids: list[MemberId]
) -> Workspace:
    return Workspace(
        owner_id=owner_id,
        _name='Full Workspace',
        _id=workspace_id,
        _description='Full Workspace description',
        logo='workspace_logo.png',
        invite_ids=[InviteId(1), InviteId(2), InviteId(3)],
        project_ids=[ProjectId(4), ProjectId(5), ProjectId(6)],
        meet_ids=[MeetId(7), MeetId(8), MeetId(9), MeetId(10)],
        tag_ids=[TagId(11), TagId(12), TagId(13), TagId(14)],
        role_ids=[RoleId(15), RoleId(16), RoleId(17), RoleId(18)],
        member_ids=two_member_ids,
    )


class TestWorkspaceCreation:

    def test_workspace_creation_with_required_data(
        self, workspace_minimal: Workspace, owner_id: OwnerId
    ) -> None:
        assert workspace_minimal.name == 'Minimal Workspace'
        assert workspace_minimal.owner_id == owner_id

    def test_workspace_creation_with_full_data(
        self, workspace_full: Workspace, two_member_ids: list[MemberId]
    ) -> None:
        assert workspace_full.name == 'Full Workspace'
        assert workspace_full.description == 'Full Workspace description'
        assert workspace_full.logo == 'workspace_logo.png'
        assert workspace_full.invite_ids == [InviteId(1), InviteId(2), InviteId(3)]
        assert workspace_full.project_ids == [ProjectId(4), ProjectId(5), ProjectId(6)]
        assert workspace_full.meet_ids == [MeetId(7), MeetId(8), MeetId(9), MeetId(10)]
        assert workspace_full.tag_ids == [TagId(11), TagId(12), TagId(13), TagId(14)]
        assert workspace_full.role_ids == [RoleId(15), RoleId(16), RoleId(17), RoleId(18)]
        assert workspace_full.member_ids == two_member_ids

    def test_workspace_has_correct_default_values(self, workspace_minimal: Workspace) -> None:
        assert workspace_minimal.description is None
        assert workspace_minimal.id is None
        assert workspace_minimal.logo is None
        assert isinstance(workspace_minimal.created_at, datetime)
        assert abs((workspace_minimal.created_at - datetime.now(timezone.utc)).total_seconds()) < 1
        assert workspace_minimal.invite_ids == []
        assert workspace_minimal.project_ids == []
        assert workspace_minimal.meet_ids == []
        assert workspace_minimal.tag_ids == []
        assert workspace_minimal.role_ids == []
        assert workspace_minimal.member_ids == []

    def test_workspace_creation_missing_required_fields(self) -> None:
        with pytest.raises(TypeError):
            Workspace()


class TestWorkspaceValidation:

    def test_valid_workspace_name(self, workspace_minimal: Workspace) -> None:
        workspace_minimal.name = 'Another Valid Workspace'
        assert workspace_minimal.name == 'Another Valid Workspace'

    def test_valid_workspace_description(self, workspace_minimal: Workspace):
        workspace_minimal.description = 'This is a valid workspace description.'
        assert workspace_minimal.description == 'This is a valid workspace description.'

    @pytest.mark.parametrize(
        'name, expected_error_message',
        [
            ('', 'Имя рабочего пространства должно содержать хотя бы одну букву'),
            (' ', 'Имя рабочего пространства должно содержать хотя бы одну букву'),
            ('Full Workspace@#$%^&*()+', 'Неверный формат названия рабочего пространства'),
        ],
    )
    def test_invalid_workspace_name(
        self, workspace_minimal: Workspace, name: str, expected_error_message: str
    ) -> None:

        with pytest.raises(ValueError, match=expected_error_message):
            workspace_minimal.name = name

    def test_invalid_workspace_description(self, workspace_minimal):
        with pytest.raises(
            ValueError,
            match=f'Длина описания рабочего пространства не должна превышать 500 символов.'
            f'И содержать только буквы латинского и русского алфавитов, включая символы пробела и -.',
        ):
            workspace_minimal.description = 'Full Workspace@#$%^&*()+'

    def test_max_workspace_name_length(self, workspace_minimal: Workspace) -> None:
        valid_name = 'n' * 50
        workspace_minimal.name = valid_name
        assert workspace_minimal.name == valid_name

        with pytest.raises(ValueError, match=f'Неверный формат названия рабочего пространства'):
            workspace_minimal.name = 'n' * 51

    def test_max_workspace_description_length(self, workspace_minimal: Workspace) -> None:
        valid_description = 'n' * 500
        workspace_minimal.description = valid_description
        assert workspace_minimal.description == valid_description

        with pytest.raises(
            ValueError,
            match=f'Длина описания рабочего пространства не должна превышать 500 символов.'
            f'И содержать только буквы латинского и русского алфавитов, включая символы пробела и -.',
        ):
            workspace_minimal.description = 'n' * 501

    def test_workspace_id_set_once_only(self, workspace_full: Workspace) -> None:
        with pytest.raises(
            AttributeError, match='Идентификатор рабочего пространства уже установлен'
        ):
            workspace_full.id = uuid4()
