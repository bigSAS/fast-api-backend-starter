from sqlalchemy import Column, Integer, ForeignKey
from app.database.setup import Base


class GroupUser(Base):
    """
    GroupUser entity. Import as GroupUserEntity.
    """
    __tablename__ = "group_users"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("user_groups.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))


"""
todo: uuid PK example

from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Foo(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


todo: add fiql example for more complex model queries
"""