from app.api.permissions import Permission
from app.api.schemas.permission import Action
from app.api.schemas.token import TokenData
from app.errors.api import ForbiddenError


class IsAdmin(Permission):
    """
    todo: ...
    """
    def check_permission(self, **kwargs):
        """
        Must be called with kwargs:
          * token_data: TokenData
        """
        token: TokenData = kwargs.get("token_data")
        # todo: find in .permissions
        print("@JWT:data", token)
        is_admin = [p for p in token.permissions if p.get('name', None) == Action.IS_ADMIN]
        if not is_admin:
            raise ForbiddenError("Admins only ... sorry :)")
