from app.database.models.user_group import UserGroup as UserGroupEntity
from app.repositories import Repository


# todo: repositories rename as not plural ex UserRepository (not UsersRepository) ect
class UserGroupsRepository(Repository):
    """
    UserGroups repository.
    """
    entity = UserGroupEntity
