from pydantic import BaseModel
from typing import Optional, List

from app.api.schemas.pagination import PaginatedModel


class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None


class NoteCreate(NoteBase): pass


class Note(NoteBase):
    id: int
    owner_id: int
    class Config: orm_mode = True


class NotesPaginated(PaginatedModel):
    """
    Note list with pagination.
    """
    items: List[Note]
    class Meta: orm_model_class = Note
