from app.database.models.group_user import GroupUser as GroupUserEntity
from app.repositories import Repository


# todo: repositories rename as not plural ex UserRepository (not UsersRepository) ect
class GroupUsersRepository(Repository):
    """
    Group Users repository.
    """
    entity = GroupUserEntity
