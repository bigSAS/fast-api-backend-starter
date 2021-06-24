from enum import Enum
from typing import NamedTuple


class PermissionDefinition(NamedTuple):
    name: str
    has_data: bool


class UserPermission(Enum):
    IS_ADMIN = PermissionDefinition(name="IS_ADMIN", has_data=False)
    IS_GROUP_MEMBER = PermissionDefinition(name="HAS_ACTION_ACCESS", has_data=True)  # ['group_a', 'group_n']
    # todo: UserGroupEntity ??? <- l8r
    HAS_ACTION_ACCESS = PermissionDefinition(name="HAS_ACTION_ACCESS", has_data=True)  # ['FOO_ACTION', 'BAR_ACTION']
    # app.permissions.Action ^
