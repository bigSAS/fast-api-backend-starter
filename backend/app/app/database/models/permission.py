from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.setup import Base


class Permission(Base):
    """
    Permission entity. Import as PermissionEntity.
    """
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # PermissionDefinition.name
    data = Column(JSONB, nullable=True)  # JSON data if needed (PermissionDefinition.has_data)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="permissions")
