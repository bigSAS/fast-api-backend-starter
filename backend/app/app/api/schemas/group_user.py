from pydantic import BaseModel
from typing import List

from app.api.schemas.pagination import PaginatedModel


class GroupUserBase(BaseModel):
    group_id: int


class GroupUserCreate(GroupUserBase):
    user_id: int


class GroupUserAddOrRemove(BaseModel):
    user_id: int


class GroupUser(GroupUserCreate):
    id: int
    class Config: orm_mode = True


class GroupUsersPaginated(PaginatedModel):
    """
    Group user list with pagination.
    """
    items: List[GroupUser]
    class Meta: orm_model_class = GroupUser
