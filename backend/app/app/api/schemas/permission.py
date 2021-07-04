from pydantic import BaseModel
from typing import Optional, List

from app.api.schemas.pagination import PaginatedModel
from enum import Enum


class Permissions(str, Enum):
    IS_ADMIN = "IS_ADMIN"
    IS_GROUP_MEMBER = "IS_GROUP_MEMBER"
    HAS_ACTION_ACCESS = "HAS_ACTION_ACCESS"


class PermissionBase(BaseModel):
    name: Permissions
    data: Optional[dict] = None


class PermissionCreate(PermissionBase):
    user_id: int

    # todo: validate permission name
    # todo: validate permission data
    # ^ 1 custom validation ? pydantic docs -> l8r


class Permission(PermissionBase):
    id: int
    user_id: int
    class Config: orm_mode = True


class PermissionsPaginated(PaginatedModel):
    """
    Note list with pagination.
    """
    items: List[Permission]
    class Meta: orm_model_class = Permission
