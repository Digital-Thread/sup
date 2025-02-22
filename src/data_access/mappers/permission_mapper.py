from src.apps.permission.domain import PermissionId
from src.apps.permission import PermissionOutputDTO
from src.data_access.models import PermissionModel


class PermissionMapper:

    @staticmethod
    def map_model_to_output_dto(model: PermissionModel) -> PermissionOutputDTO:
        return PermissionOutputDTO(
            id=PermissionId(model.id),
            description=model.description,
        )
