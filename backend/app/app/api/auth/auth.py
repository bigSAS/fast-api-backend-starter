from passlib.context import CryptContext
from jose import jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from app.errors.api import AuthError
from app.database.models.user import User
from app.repositories.users import UserRepository

SECRET_KEY = "e41fae79f843957edfc3d3221bc58af4cf3d03a48c77e86f5d02c7f807f8194b"  # todo: config / env var?
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # todo: config / env var?


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def _is_password_valid(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session = Depends()) -> User:
    user = UserRepository(db).get_by(username=username, ignore_not_found=True)
    if not user: raise AuthError('Invalid username or password')
    if not _is_password_valid(password, user.hashed_password): raise AuthError('Invalid username or password')
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
