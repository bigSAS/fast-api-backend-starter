from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.setup import Base


class User(Base):
    """
    User entity. Import as UserEntity
    # todo: refactor naming, find usages and import as
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    notes = relationship("Note", back_populates="owner",
                         cascade="all, delete")
