from app.database.models.user import User as UserEntity
from app.repositories import Repository


class UserRepository(Repository):
    entity = UserEntity

    def delete(self, entity_id: int):
        raise ValueError('User repositories cannot delete users!')  # todo: adapt errors package (Repository Error after repository errors done)
