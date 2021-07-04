from sqlalchemy import Column, Integer, ForeignKey
from app.database.setup import Base
from sqlalchemy.orm import relationship


class GroupUser(Base):
    """
    GroupUser entity. Import as GroupUserEntity.
    """
    __tablename__ = "group_users"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("user_groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
