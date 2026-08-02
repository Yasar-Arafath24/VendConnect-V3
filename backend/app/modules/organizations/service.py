from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.organizations.model import Organization
from app.modules.organizations.repository import OrganizationRepository
from app.modules.organizations.schema import OrganizationCreate


class OrganizationService:

    @staticmethod
    def generate_organization_code() -> str:
        """
        Generates a unique organization code.
        Example: VC8A3F2D
        """
        return f"VC{str(uuid4()).replace('-', '')[:6].upper()}"

    @staticmethod
    def create_organization(
        db: Session,
        organization_data: OrganizationCreate,
    ) -> Organization:

        # Check duplicate email
        existing = OrganizationRepository.get_by_email(
            db,
            organization_data.email,
        )

        if existing:
            raise ValueError("Organization with this email already exists.")

        organization = Organization(
            organization_code=OrganizationService.generate_organization_code(),
            organization_name=organization_data.organization_name,
            owner_name=organization_data.owner_name,
            email=organization_data.email,
            phone=organization_data.phone,
        )

        return OrganizationRepository.create(db, organization)

    @staticmethod
    def get_organization(
        db: Session,
        organization_id: str,
    ):
        return OrganizationRepository.get_by_id(db, organization_id)

    @staticmethod
    def list_organizations(db: Session):
        return OrganizationRepository.get_all(db)