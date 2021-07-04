from pydantic import BaseModel
from typing import Optional, List

from app.api.schemas.pagination import PaginatedModel


class UserGroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class UserGroupCreate(UserGroupBase):
    # todo: validate unique name
    pass


class UserGroup(UserGroupBase):
    id: int
    class Config: orm_mode = True


class UserGroupsPaginated(PaginatedModel):
    """
    Note list with pagination.
    """
    items: List[UserGroup]
    class Meta: orm_model_class = UserGroup
