from enum import Enum

from pydantic import BaseModel
from typing import Optional, List

from app.api.schemas.pagination import PaginatedModel


class Action(str, Enum):
    """
    Actions enum for naming permissions
    """
    IS_ADMIN = "IS_ADMIN"  # is admin user, can do anything LOL
    # todo: rest of api actions
    FOO_ACTION = "FOO_ACTION"
    BAR_ACTION = "BAR_ACTION"


class PermissionBase(BaseModel):
    name: Action
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
