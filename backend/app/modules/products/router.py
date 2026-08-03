from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.auth.dependencies import (
    get_current_user,
    require_permission,
)

from app.modules.products.schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.modules.products.service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product:create")
    ),
):
    try:
        return ProductService.create(
            db=db,
            product_data=product,
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
    response_model=list[ProductResponse],
)
def get_products(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product:view")
    ),
):
    return ProductService.get_all(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product:view")
    ),
):
    product = ProductService.get_by_id(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: str,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product:update")
    ),
):
    try:
        return ProductService.update(
            db=db,
            product_id=product_id,
            product_data=product,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
        

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product:delete")
    ),
):
    try:
        return ProductService.delete(
            db,
            product_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
        
