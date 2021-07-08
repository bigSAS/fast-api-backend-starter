from app.database.models.permission import Permission as PermissionEntity
from app.repositories import Repository


# todo: repositories rename as not plural ex UserRepository (not UsersRepository) ect
class PermissionsRepository(Repository):
    """
    Permissions repository.
    """
    entity = PermissionEntity
