from app.database.models.permission import Permission as PermissionEntity
from app.repositories import Repository


class PermissionsRepository(Repository):
    """
    Permissions repository.
    """
    entity = PermissionEntity
