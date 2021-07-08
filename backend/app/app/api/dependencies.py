from starlette.requests import Request

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.api.schemas.token import TokenData
from app.api.auth.auth import SECRET_KEY, ALGORITHM
from app.database.setup import SessionLocal
from app.errors.api import AuthError
from app.database.models.user import User as UserEntity

from app.repositories.users import UserRepository


def get_db():
    """
    DB dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise AuthError('Not authenticated')


oauth2_scheme = AuthBearer(tokenUrl="token")


def authenticated_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserEntity:
    """
    User for JWT protected endpoints
    """
    auth_error = AuthError("Invalid JWT")
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        print("@token:", token_data)
    except JWTError:
        raise auth_error
    user = UserRepository(db).get_by(username=token_data.username, ignore_not_found=True)
    if user is None:
        raise auth_error
    return user


class Restricted(object):
    """
    Permission dependency.
    Example:
        @router.post("/url", tags=['foo'],
             response_model=Foo,
             responses=res.AUTHENTICATED | res.PROTECTED,
             dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
             ])
    """

    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    async def __call__(self, request: Request):
        token = oauth2_scheme
        decoded_token = jwt.decode(await token(request), key=SECRET_KEY, algorithms=[ALGORITHM])
        token_data: TokenData = TokenData(**decoded_token)
        for permission_class in self.permissions_classes:  # permission must be a app.api.permissions.Permission
            permission_class().check_permission(request=request, token_data=token_data)
