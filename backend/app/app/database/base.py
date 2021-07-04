"""
Imports 4 alembic
"""
from app.database.setup import Base
from app.database.models.user import User as UserEntity
from app.database.models.note import Note as NoteEntity
from app.database.models.permission import Permission as PermissionEntity
