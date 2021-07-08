from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routers import responses as res
from app.api.permissions.user_permissions import IsAdmin

from app.api.dependencies import get_db, authenticated_user, Restricted
from app.api.schemas.user_group import UserGroupsPaginated, UserGroupCreate, UserGroup
from app.api.schemas.group_user import GroupUser, GroupUserAddOrRemove, GroupUsersPaginated
from app.database.models.user_group import UserGroup as UserGroupEntity
from app.database.models.group_user import GroupUser as GroupUserEntity
from app.repositories.user_groups import UserGroupsRepository
from app.repositories.group_users import GroupUsersRepository
from app.repositories.users import UserRepository

router = APIRouter()


@router.get("/user-groups", tags=['admin'],
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


@router.post("/user-groups", tags=['admin'],
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


@router.delete("/user-groups", tags=['admin'],
               status_code=204,
               responses=res.AUTHENTICATED | res.PROTECTED,
               dependencies=[
                   Depends(authenticated_user),
                   Depends(Restricted([IsAdmin]))
               ])
async def delete_user_group(
        group_id: int,
        db: Session = Depends(get_db)):
    """
    Delete user group.
    """
    UserGroupsRepository(db).delete(group_id)
    return None


@router.post("/user-groups/{group_id}/add-user", tags=['admin'],
             response_model=GroupUser,
             responses=res.AUTHENTICATED | res.PROTECTED,
             dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
             ])
async def add_user_to_group(
        group_id: int,
        group_user_add: GroupUserAddOrRemove,
        db: Session = Depends(get_db)):
    """
    Add user to group.
    todo: add only if not already added
    """
    group = UserGroupsRepository(db).get(group_id)
    user = UserRepository(db).get(group_user_add.user_id)
    new_group_user = GroupUserEntity(
        group_id=group.id,
        user_id=user.id
    )
    GroupUsersRepository(db).save(new_group_user)
    return new_group_user


@router.post("/user-groups/{group_id}/remove-user", tags=['admin'],
             status_code=204,
             responses=res.AUTHENTICATED | res.PROTECTED,
             dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
             ])
async def remove_user_from_group(
        group_id: int,
        group_user_add: GroupUserAddOrRemove,
        db: Session = Depends(get_db)):
    """
    Remove user from group.
    """
    user = UserRepository(db).get(group_user_add.user_id)
    group_user = GroupUsersRepository(db).get_by(group_id=group_id, user_id=user.id)
    GroupUsersRepository(db).delete(group_user.id)
    return None


@router.get("/user-groups/{group_id}/group-users", tags=['admin'],
            response_model=GroupUsersPaginated,
            responses=res.AUTHENTICATED | res.PROTECTED,
            dependencies=[
                Depends(authenticated_user),
                Depends(Restricted([IsAdmin]))
            ])
async def list_group_users(
        group_id: int,
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    List group users by group id..
    """
    return GroupUsersPaginated.from_paginated_query(
        GroupUsersRepository(db).filter_paginated(
            GroupUserEntity.group_id == group_id, page=page, limit=limit, order=order_by)
    )


@router.get("/user-groups/me", tags=['admin'],  # todo: new scope - logged in user instead of admin
            response_model=GroupUsersPaginated,
            responses=res.AUTHENTICATED | res.PROTECTED,
            dependencies=[
                Depends(Restricted([]))
            ])
async def list_my_user_groups(
        user=Depends(authenticated_user),
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    List user groups of authenticated user.
    """
    return GroupUsersPaginated.from_paginated_query(
        GroupUsersRepository(db).filter_paginated(
            GroupUserEntity.user_id == user.id, page=page, limit=limit, order=order_by)
    )
