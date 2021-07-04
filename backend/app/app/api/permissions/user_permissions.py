from app.api.permissions import BasePermission
from app.api.schemas.permission import Permissions
from app.api.schemas.token import TokenData
from app.errors.api import ForbiddenError


class IsAdmin(BasePermission):
    """
    Check if JWT user is admin.
    """
    def check_permission(self, **kwargs):
        """
        Must be called with kwargs:
          * token_data: TokenData
        """
        token: TokenData = kwargs.get("token_data")
        is_admin = [p for p in token.permissions if p.get('name', None) == Permissions.IS_ADMIN]
        if not is_admin:
            raise ForbiddenError("Admins only ... sorry :)")
