from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.api.routers import responses as res
from app.api.permissions.user_permissions import IsAdmin
from app.database.models.user import User as UserModel
from app.api.auth import auth
from app.api.dependencies import get_db, authenticated_user, Restricted
from app.api.schemas.user import User, UserCreate, UsersPaginated
from app.errors.api import ErrorMessage, BadRequestError
from app.repositories.permissions import PermissionsRepository
from app.repositories.users import UserRepository
from app.services.messaging.email import send_email
from app.config import settings

from app.database.models.permission import Permission as PermissionEntity


router = APIRouter()


# todo: update responses and permissions similat to permissions router

@router.post("/token", tags=['auth'],
             responses={400: {'model': ErrorMessage}})
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    todo: docstring
    """
    user = auth.authenticate_user(db=db, username=form_data.username, password=form_data.password)

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_permissions = PermissionsRepository(db).filter(PermissionEntity.user_id == user.id)
    data = {
        'username': user.username,
        'permissions': [{'name': permission.name, 'data': permission.data} for permission in user_permissions]
    }
    access_token = auth.create_access_token(data=data, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", tags=['admin'],
            response_model=UsersPaginated,
            dependencies=[Depends(authenticated_user)])
def list_users(page: int = 0, limit: int = 100, order_by: str = None, db: Session = Depends(get_db)):
    """
    List all users with pagination.
    """
    return UsersPaginated.from_paginated_query(
        UserRepository(db).all_paginated(
            page=page,
            limit=limit,
            order=order_by
        )
    )


@router.get("/users/me", tags=['users'],
            response_model=User)
def get_request_user(current_user: User = Depends(authenticated_user)):
    """
    todo: docstring
    """
    return current_user


@router.get("/users/{user_id}", tags=['users'],
            response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    todo: docstring
    """
    return UserRepository(db).get(entity_id=user_id)

# todo: refactor rest using repository


@router.post("/users", tags=['users'],
             response_model=User)
def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    db_user = user_repository.get_by(email=user.email, ignore_not_found=True)
    if db_user:
        raise BadRequestError("Email already registered")

    # todo: check this l8r
    if settings.SMTP_SERVER != "your_stmp_server_here":
        background_tasks.add_task(send_email, user.email,
                                  message=f"You've created your account!")
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=auth.get_password_hash(user.password)
    )
    user_repository.save(new_user)
    return new_user


@router.delete("/users/{user_id}", tags=['admin'],
               status_code=204,
               response_model=None,
               responses=res.AUTHENTICATED | res.PROTECTED | res.NO_CONTENT,
               dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
               ])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # todo: do not delete user objects, add property deleted (boolean)
    user = UserRepository(db).get(user_id)
    # todo: soft delete user (.deleted=True)
    print(user)
    return None
