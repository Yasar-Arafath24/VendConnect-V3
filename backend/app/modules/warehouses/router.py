from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.warehouses.schema import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse,
    WarehouseListResponse,
)
from app.modules.warehouses.service import WarehouseService

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"],
)


@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("warehouse:create")
    ),
):
    try:
        return WarehouseService.create(
            db=db,
            warehouse_data=warehouse,
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
    response_model=WarehouseListResponse,
)
def get_warehouses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("warehouse:view")
    ),
):
    return WarehouseService.get_all(
        db=db,
        organization_id=current_user.organization_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/search/",
    response_model=list[WarehouseResponse],
)
def search_warehouses(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("warehouse:view")
    ),
):
    return WarehouseService.search(
        db,
        current_user.organization_id,
        keyword,
    )


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
)
def get_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("warehouse:view")
    ),
):
    warehouse = WarehouseService.get_by_id(
        db,
        warehouse_id,
    )

    if warehouse is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found.",
        )

    return warehouse


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
)
def update_warehouse(
    warehouse_id: str,
    warehouse: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("warehouse:update")
    ),
):
    try:
        return WarehouseService.update(
            db=db,
            warehouse_id=warehouse_id,
            warehouse_data=warehouse,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{warehouse_id}")
def delete_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("warehouse:delete")
    ),
):
    try:
        return WarehouseService.delete(
            db,
            warehouse_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
