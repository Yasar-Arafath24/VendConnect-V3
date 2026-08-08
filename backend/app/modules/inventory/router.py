from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.inventory.schema import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryListResponse,
    StockAdjustment,
    StockTransfer,
)
from app.modules.inventory.service import InventoryService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post(
    "/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:create")
    ),
):
    try:
        return InventoryService.create(
            db=db,
            inventory_data=inventory,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=InventoryListResponse,
)
def get_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:view")
    ),
):
    return InventoryService.get_all(
        db=db,
        organization_id=current_user.organization_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/low-stock",
    response_model=list[InventoryResponse],
)
def get_low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:view")
    ),
):
    return InventoryService.get_low_stock(
        db,
        current_user.organization_id,
    )


@router.post(
    "/transfer",
    status_code=status.HTTP_200_OK,
)
def transfer_stock(
    transfer: StockTransfer,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:update")
    ),
):
    try:
        return InventoryService.transfer_stock(
            db=db,
            transfer=transfer,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.put(
    "/{inventory_id}/adjust",
    response_model=InventoryResponse,
)
def adjust_stock(
    inventory_id: str,
    adjustment: StockAdjustment,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:update")
    ),
):
    try:
        return InventoryService.adjust_stock(
            db=db,
            inventory_id=inventory_id,
            adjustment=adjustment,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse,
)
def get_inventory_by_id(
    inventory_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:view")
    ),
):
    inventory = InventoryService.get_by_id(
        db,
        inventory_id,
        current_user.organization_id,
    )

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found.",
        )

    return inventory


@router.put(
    "/{inventory_id}",
    response_model=InventoryResponse,
)
def update_inventory(
    inventory_id: str,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:update")
    ),
):
    try:
        return InventoryService.update(
            db=db,
            inventory_id=inventory_id,
            inventory_data=inventory,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory:delete")
    ),
):
    try:
        return InventoryService.delete(
            db,
            inventory_id,
            current_user.organization_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
