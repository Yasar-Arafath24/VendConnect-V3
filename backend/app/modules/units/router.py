from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.units.schema import (
    UnitCreate,
    UnitListResponse,
    UnitResponse,
    UnitUpdate,
)
from app.modules.units.service import UnitService

router = APIRouter(
    prefix="/units",
    tags=["Units"],
)


@router.post(
    "",
    response_model=UnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_unit(
    unit: UnitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("unit:create")
    ),
):
    try:
        return UnitService.create(
            db=db,
            unit_data=unit,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "",
    response_model=UnitListResponse,
)
def get_units(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("unit:view")
    ),
):
    return UnitService.get_all(
        db,
        current_user.organization_id,
        skip,
        limit,
    )


@router.get(
    "/search",
    response_model=list[UnitResponse],
)
def search_units(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("unit:view")
    ),
):
    return UnitService.search(
        db,
        current_user.organization_id,
        keyword,
    )


@router.get(
    "/{unit_id}",
    response_model=UnitResponse,
)
def get_unit(
    unit_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("unit:view")
    ),
):
    unit = UnitService.get_by_id(
        db,
        unit_id,
    )

    if unit is None:
        raise HTTPException(
            status_code=404,
            detail="Unit not found.",
        )

    return unit


@router.put(
    "/{unit_id}",
    response_model=UnitResponse,
)
def update_unit(
    unit_id: str,
    unit: UnitUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("unit:update")
    ),
):
    try:
        return UnitService.update(
            db=db,
            unit_id=unit_id,
            unit_data=unit,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{unit_id}")
def delete_unit(
    unit_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("unit:delete")
    ),
):
    try:
        return UnitService.delete(
            db,
            unit_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
