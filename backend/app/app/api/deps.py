from typing import Optional
from starlette.requests import Request

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.api.schemas.token import TokenData
from app.crud import crud_user
from app.api.auth.auth import SECRET_KEY, ALGORITHM
from app.database.setup import SessionLocal
from app.errors.api import AuthError
from app.models.user import User


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


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    auth_error = AuthError("Invalid JWT")
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise auth_error
        token_data = TokenData(username=username)
    except JWTError:
        raise auth_error
    user = crud_user.get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise auth_error
    return user
