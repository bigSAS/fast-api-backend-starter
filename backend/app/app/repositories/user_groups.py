from app.database.models.user_group import UserGroup as UserGroupEntity
from app.repositories import Repository


class UserGroupsRepository(Repository):
    """
    UserGroups repository.
    """
    entity = UserGroupEntity
