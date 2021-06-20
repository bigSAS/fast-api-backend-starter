from app.models.user import User
from app.repositories import Repository


class UserRepository(Repository):
    entity = User

    def delete(self, entity_id: int):
        raise ValueError('User repositories cannot delete users!')  # todo: adapt errors package
