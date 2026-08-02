from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.organizations.schema import (
    OrganizationCreate,
    OrganizationResponse,
)
from app.modules.organizations.service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=201,
)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
):
    try:
        return OrganizationService.create_organization(
            db,
            organization,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[OrganizationResponse],
)
def get_all_organizations(
    db: Session = Depends(get_db),
):
    return OrganizationService.list_organizations(db)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: str,
    db: Session = Depends(get_db),
):
    organization = OrganizationService.get_organization(
        db,
        organization_id,
    )

    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    return organization