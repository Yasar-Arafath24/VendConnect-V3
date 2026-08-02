from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.rbac.user_role_schema import (
    AssignRoleRequest,
)
from app.modules.rbac.user_role_service import (
    UserRoleService,
)

router = APIRouter(
    prefix="/user-roles",
    tags=["User Roles"],
)


@router.post("/")
def assign_role(
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
):
    try:
        return UserRoleService.assign_role(
            db,
            request.user_id,
            request.role_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/{user_id}")
def get_roles(
    user_id: str,
    db: Session = Depends(get_db),
):
    return UserRoleService.get_roles(
        db,
        user_id,
    )


@router.delete("/")
def remove_role(
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
):
    success = UserRoleService.remove_role(
        db,
        request.user_id,
        request.role_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Role assignment not found.",
        )

    return {"message": "Role removed successfully."}