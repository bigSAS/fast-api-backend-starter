from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routers import responses as res
from app.api.permissions.user_permissions import IsAdmin

from app.api.dependencies import get_db, authenticated_user, Restricted
from app.api.schemas.user_group import UserGroupsPaginated, UserGroupCreate, UserGroup
from app.database.models.user_group import UserGroup as UserGroupEntity
from app.repositories.user_groups import UserGroupsRepository

router = APIRouter()


@router.get("/user_groups", tags=['admin'],
            response_model=UserGroupsPaginated,
            responses=res.AUTHENTICATED | res.PROTECTED,
            dependencies=[
                Depends(authenticated_user),
                Depends(Restricted([IsAdmin]))
            ])
async def list_user_groups(
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    List user groups paginated.
    """
    return UserGroupsPaginated.from_paginated_query(
        UserGroupsRepository(db).all_paginated(page=page, limit=limit, order=order_by)
    )


@router.post("/user_groups", tags=['admin'],
             response_model=UserGroup,
             responses=res.AUTHENTICATED | res.PROTECTED,
             dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
             ])
async def create_user_group(
        user_group: UserGroupCreate,
        db: Session = Depends(get_db)):
    """
    Create user group.
    """
    new_group = UserGroupEntity(
        name=user_group.name,
        description=user_group.description
    )
    UserGroupsRepository(db).save(new_group)
    return new_group


# async def delete_user_group <- todo
# async def add_user_to_group <- todo user_id, group_id
# async def remove_user_from_group <- todo user_id, group_id
# async def get_user_goups <- todo by user_id <- no admin
# async def get_gourp_users <- todo by group id <- no admin
# async def get_my_user_groups <- todo by token
