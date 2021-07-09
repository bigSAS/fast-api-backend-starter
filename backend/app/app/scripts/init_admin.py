from app.api.auth import auth
from app.database.models.permission import Permission as PermissionEntity
from app.database.models.user import User as UserEntity
from app.database.setup import SessionLocal
from app.repositories.permissions import PermissionsRepository
from app.repositories.users import UserRepository


def init_admin():
    db = SessionLocal()
    user_repository = UserRepository(db)
    admin = user_repository.get_by(username='admin', ignore_not_found=True)
    if not admin:
        print("No admin fund setting default admin:admin\nCHANGE PSSWD ASAP!!!")
        default_admin = UserEntity(
            username='admin',
            email='admin',
            hashed_password=auth.get_password_hash('admin')
        )
        user_repository.save(default_admin)
        admin_permission = PermissionEntity(
            name="IS_ADMIN",
            user_id=default_admin.id
        )
        PermissionsRepository(db).save(admin_permission)
        print("Done.")
    else:
        print("Skipping adding admin user")


if __name__ == '__main__': init_admin()
