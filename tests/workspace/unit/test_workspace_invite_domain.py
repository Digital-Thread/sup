from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from src.apps.workspace.domain.entities.workspace_invite import (
    StatusInvite,
    WorkspaceInviteEntity,
)
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from tests.fixtures.workspace_fixtures import invite_code, workspace_id


@pytest.fixture()
def workspace_invite_minimal(workspace_id: WorkspaceId) -> WorkspaceInviteEntity:
    return WorkspaceInviteEntity(
        _workspace_id=workspace_id,
    )


@pytest.fixture()
def workspace_invite_full(workspace_id: WorkspaceId, invite_code: UUID) -> WorkspaceInviteEntity:
    return WorkspaceInviteEntity(
        _workspace_id=workspace_id,
        _id=InviteId(1),
        code=invite_code,
        _status=StatusInvite.ACTIVE,
        created_at=datetime.now(timezone.utc),
    )


class TestWorkspaceInviteCreation:

    def test_workspace_invite_creation_with_required_data(
        self, workspace_invite_minimal: WorkspaceInviteEntity, workspace_id: WorkspaceId
    ) -> None:
        assert workspace_invite_minimal.workspace_id == workspace_id

    def test_workspace_invite_creation_with_full_data(
        self, workspace_invite_full: WorkspaceInviteEntity, workspace_id: WorkspaceId, invite_code: UUID
    ) -> None:
        assert workspace_invite_full.workspace_id == workspace_id
        assert workspace_invite_full._id == InviteId(1)
        assert workspace_invite_full._status == StatusInvite.ACTIVE
        assert workspace_invite_full.code == invite_code

    def test_workspace_invite_has_correct_default_values(
        self, workspace_invite_minimal: WorkspaceInviteEntity
    ) -> None:
        assert workspace_invite_minimal.id is None
        assert workspace_invite_minimal.code is not None and isinstance(
            workspace_invite_minimal.code, UUID
        )
        assert workspace_invite_minimal.status == StatusInvite.ACTIVE
        assert isinstance(workspace_invite_minimal.created_at, datetime)
        assert (
            abs((workspace_invite_minimal.created_at - datetime.now(timezone.utc)).total_seconds())
            < 1
        )
        assert (
            workspace_invite_minimal.expired_at
            == workspace_invite_minimal.created_at + timedelta(days=WorkspaceInviteEntity.EXPIRATION_DAYS)
        )

    def test_workspace_invite_creation_missing_required_fields(self) -> None:
        with pytest.raises(TypeError):
            WorkspaceInviteEntity()


class TestWorkspaceInviteValidation:

    def test_workspace_invite_valid_change_status(
        self, workspace_invite_minimal: WorkspaceInviteEntity
    ) -> None:
        workspace_invite_minimal.use()

        workspace_invite_minimal._expired_at = datetime.now(
            timezone.utc
        )  # имитируем истечение срока ссылки
        workspace_invite_minimal.expire()

    def test_workspace_invite_invalid_change_status(
        self, workspace_invite_minimal: WorkspaceInviteEntity
    ) -> None:
        with pytest.raises(ValueError, match='Статус уже установлен'):
            workspace_invite_minimal.activate()

        with pytest.raises(ValueError, match='Приглашение ещё не истекло'):
            workspace_invite_minimal.expire()

    def test_workspace_invite_id_set_once_only(
        self, workspace_invite_full: WorkspaceInviteEntity
    ) -> None:
        with pytest.raises(AttributeError, match='Идентификатор ссылки приглашения уже установлен'):
            workspace_invite_full.id = 2
