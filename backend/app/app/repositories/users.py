from app.database.models.user import User as UserEntity
from app.repositories import Repository


class UserRepository(Repository):
    entity = UserEntity

    def delete(self, entity_id: int):
        user: UserEntity = self.get(entity_id)
        user.is_deleted = True
        self.save(user)
