from typing import List

from pydantic import BaseModel
from app.api.schemas.pagination import PaginatedModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_deleted: bool
    class Config: orm_mode = True


class UsersPaginated(PaginatedModel):
    """
    User list with pagination.
    """
    items: List[User]
    class Meta: orm_model_class = User
