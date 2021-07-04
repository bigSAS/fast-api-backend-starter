from sqlalchemy import Column, String, Integer
from app.database.setup import Base


class UserGroup(Base):
    """
    UserGroup entity. Import as UserGroupEntity.
    """
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, nullable=True)
