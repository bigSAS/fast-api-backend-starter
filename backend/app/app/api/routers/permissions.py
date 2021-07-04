from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routers import responses as res
from app.api.permissions.user_permissions import IsAdmin
from app.api.schemas.permission import PermissionsPaginated, PermissionCreate, Permission
from app.api.dependencies import get_db, authenticated_user, Restricted
from app.database.models.permission import Permission as PermissionEntity
from app.repositories.permissions import PermissionsRepository

router = APIRouter()


@router.get("/permissions", tags=['admin'],
            response_model=PermissionsPaginated,
            responses=res.AUTHENTICATED | res.PROTECTED,
            dependencies=[
                Depends(authenticated_user),
                Depends(Restricted([IsAdmin]))
            ])
async def list_permissions(
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    List permissions paginated.
    """
    return PermissionsPaginated.from_paginated_query(
        PermissionsRepository(db).all_paginated(page=page, limit=limit, order=order_by)
    )


@router.get("/permissions/{user_id}", tags=['admin'],
            response_model=PermissionsPaginated,
            responses=res.AUTHENTICATED | res.PROTECTED,
            dependencies=[
                Depends(authenticated_user),
                Depends(Restricted([IsAdmin]))
            ])
async def list_user_permissions(
        user_id: int,
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    List user permissions paginated (by user id).
    """
    return PermissionsPaginated.from_paginated_query(
        PermissionsRepository(db).filter_paginated(
            PermissionEntity.user_id == user_id,
            page=page,
            limit=limit,
            order=order_by
        )
    )


@router.post("/permissions", tags=['admin'],
             response_model=Permission,
             responses=res.AUTHENTICATED | res.PROTECTED,
             dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
             ])
async def create_permission(
        permission: PermissionCreate,
        db: Session = Depends(get_db)):
    """
    Create permission
    """
    new_permission = PermissionEntity(
        user_id=permission.user_id,
        name=permission.name,
        data=permission.data
    )
    PermissionsRepository(db).save(new_permission)
    return new_permission


@router.delete("/permissions/{permission_id}", tags=['admin'],
               status_code=204,
               response_model=None,
               responses=res.AUTHENTICATED | res.PROTECTED | res.NO_CONTENT,
               dependencies=[
                 Depends(authenticated_user),
                 Depends(Restricted([IsAdmin]))
               ])
async def delete_permission(
        permission_id: int,
        db: Session = Depends(get_db)):
    """
    Delete permission by id.
    """
    PermissionsRepository(db).delete(permission_id)
    return ''
