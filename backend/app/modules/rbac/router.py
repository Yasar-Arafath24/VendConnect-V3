from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.rbac.schema import (
    AssignPermission,
    PermissionCreate,
    PermissionResponse,
    RoleCreate,
    RoleResponse,
)
from app.modules.rbac.service import RBACService

router = APIRouter(
    prefix="/rbac",
    tags=["RBAC"],
)


# ==========================
# Roles
# ==========================

@router.post(
    "/roles",
    response_model=RoleResponse,
    status_code=201,
)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
):
    try:
        return RBACService.create_role(
            db=db,
            name=role.name,
            description=role.description,
            organization_id=role.organization_id,
            is_system=role.is_system,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get(
    "/roles",
    response_model=list[RoleResponse],
)
def get_roles(
    db: Session = Depends(get_db),
):
    return RBACService.get_roles(db)


# ==========================
# Permissions
# ==========================

@router.post(
    "/permissions",
    response_model=PermissionResponse,
    status_code=201,
)
def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
):
    try:
        return RBACService.create_permission(
            db=db,
            key=permission.key,
            resource=permission.resource,
            action=permission.action,
            description=permission.description,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get(
    "/permissions",
    response_model=list[PermissionResponse],
)
def get_permissions(
    db: Session = Depends(get_db),
):
    return RBACService.get_permissions(db)


# ==========================
# Assign Permission
# ==========================

@router.post(
    "/roles/{role_name}/permissions",
)
def assign_permission(
    role_name: str,
    request: AssignPermission,
    db: Session = Depends(get_db),
):
    try:
        RBACService.assign_permission(
            db,
            role_name,
            request.permission_key,
        )

        return {
            "message": "Permission assigned successfully."
        }

    except ValueError as e:
        raise HTTPException(400, detail=str(e))