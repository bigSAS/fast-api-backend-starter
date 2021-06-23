from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.database.models.user import User as UserModel
from app.api.auth import auth
from app.api.deps import get_db, authenticated_user
from app.api.schemas.user import User, UserCreate, UsersPaginated
from app.errors.api import ErrorMessage, BadRequestError
from app.repositories.users import UserRepository
from app.services.messaging.email import send_email
from app.config import settings


router = APIRouter()


@router.post("/token", tags=['auth'],
             responses={400: {'model': ErrorMessage}})
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    todo: docstring
    """
    user = auth.authenticate_user(db=db, username=form_data.username, password=form_data.password)

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
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


@router.delete("/users/{user_id}", tags=['admin'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # todo: do not delete user objects, add property deleted (boolean)
    user = UserRepository(db).get(user_id)
    # todo: soft delete user (.deleted=True)
    print(user)
    return {"detail": f"User with id {user_id} successfully deleted"}
