from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.categories.schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.modules.categories.service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("category:create")
    ),
):
    try:
        return CategoryService.create(
            db=db,
            category_data=category,
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
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("category:view")
    ),
):
    return CategoryService.get_all(
        db,
        current_user.organization_id,
    )

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("category:view")
    ),
):
    category = CategoryService.get_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found.",
        )

    return category

@router.get(
    "/search/",
    response_model=list[CategoryResponse],
)
def search_categories(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("category:view")
    ),
):
    return CategoryService.search(
        db,
        current_user.organization_id,
        keyword,
    )
    

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: str,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("category:update")
    ),
):
    try:
        return CategoryService.update(
            db=db,
            category_id=category_id,
            category_data=category,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("category:delete")
    ),
):
    try:
        return CategoryService.delete(
            db,
            category_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
