from typing import Optional
from starlette.requests import Request

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.api.schemas.token import TokenData
from app.api.auth.auth import SECRET_KEY, ALGORITHM
from app.database.setup import SessionLocal
from app.errors.api import AuthError
from app.database.models.user import User

# todo: move to auth ?
# todo: get_db move to database package ?
from app.repositories.users import UserRepository


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise AuthError('Not authenticated')


oauth2_scheme = AuthBearer(tokenUrl="token")


def authenticated_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    todo: docs
    """
    auth_error = AuthError("Invalid JWT")
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise auth_error
        token_data = TokenData(username=username)
    except JWTError:
        raise auth_error
    user = UserRepository(db).get_by(username=token_data.username, ignore_not_found=True)
    if user is None:
        raise auth_error
    return user
