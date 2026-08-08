from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.inventory.movement_schema import (
    InventoryMovementListResponse,
    InventoryMovementResponse,
)
from app.modules.inventory.movement_service import (
    InventoryMovementService,
)


router = APIRouter(
    prefix="/inventory/movements",
    tags=["Inventory Movements"],
)

#get all movement history
@router.get(
    "/",
    response_model=InventoryMovementListResponse,
)
def get_movements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:view")
    ),
):
    return InventoryMovementService.get_all(
        db=db,
        organization_id=current_user.organization_id,
        skip=skip,
        limit=limit,
    )
    
#get movement by id
@router.get(
    "/{movement_id}",
    response_model=InventoryMovementResponse,
)
def get_movement(
    movement_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:view")
    ),
):
    movement = InventoryMovementService.get_by_id(
        db=db,
        movement_id=movement_id,
        organization_id=current_user.organization_id,
    )

    if movement is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory movement not found.",
        )

    return movement