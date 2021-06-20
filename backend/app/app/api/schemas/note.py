from pydantic import BaseModel
from typing import Optional


class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteSchema(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
