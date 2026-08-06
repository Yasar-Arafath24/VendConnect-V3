from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.brands.schema import (
    BrandCreate,
    BrandListResponse,
    BrandResponse,
    BrandUpdate,
)
from app.modules.brands.service import BrandService

router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
)


@router.post(
    "",
    response_model=BrandResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("brand:create")
    ),
):
    try:
        return BrandService.create(
            db=db,
            brand_data=brand,
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
    response_model=BrandListResponse,
)
def get_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("brand:view")
    ),
):
    return BrandService.get_all(
        db,
        current_user.organization_id,
        skip,
        limit,
    )


@router.get(
    "/search",
    response_model=list[BrandResponse],
)
def search_brands(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("brand:view")
    ),
):
    return BrandService.search(
        db,
        current_user.organization_id,
        keyword,
    )


@router.get(
    "/{brand_id}",
    response_model=BrandResponse,
)
def get_brand(
    brand_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("brand:view")
    ),
):
    brand = BrandService.get_by_id(
        db,
        brand_id,
    )

    if brand is None:
        raise HTTPException(
            status_code=404,
            detail="Brand not found.",
        )

    return brand


@router.put(
    "/{brand_id}",
    response_model=BrandResponse,
)
def update_brand(
    brand_id: str,
    brand: BrandUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("brand:update")
    ),
):
    try:
        return BrandService.update(
            db=db,
            brand_id=brand_id,
            brand_data=brand,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{brand_id}")
def delete_brand(
    brand_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("brand:delete")
    ),
):
    try:
        return BrandService.delete(
            db,
            brand_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
