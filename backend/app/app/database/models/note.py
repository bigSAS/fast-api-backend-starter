from sqlalchemy import Column, String, Integer, ForeignKey
from app.database.setup import Base


class Note(Base):
    """
    Note entity. Import as NoteEntity.
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
