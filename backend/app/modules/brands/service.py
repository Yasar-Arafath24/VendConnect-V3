from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.brands.model import Brand
from app.modules.brands.repository import BrandRepository
from app.modules.brands.schema import (
    BrandCreate,
    BrandUpdate,
)
from app.modules.organizations.repository import (
    OrganizationRepository,
)


class BrandService:

    @staticmethod
    def create(
        db: Session,
        brand_data: BrandCreate,
        organization_id: str,
        user_id: str,
    ) -> Brand:

        # Validate organization
        organization = OrganizationRepository.get_by_id(
            db,
            organization_id,
        )

        if organization is None:
            raise ValueError(
                "Organization not found."
            )

        # Prevent duplicate names
        existing = BrandRepository.get_by_name(
            db,
            organization_id,
            brand_data.name,
        )

        if existing:
            raise ValueError(
                "Brand already exists."
            )

        brand = Brand(
            id=str(uuid4()),
            organization_id=organization_id,

            name=brand_data.name,
            description=brand_data.description,
            logo_url=brand_data.logo_url,
            is_active=brand_data.is_active,

            created_by=user_id,
            updated_by=user_id,
        )

        return BrandRepository.create(
            db,
            brand,
        )

    @staticmethod
    def get_by_id(
        db: Session,
        brand_id: str,
    ):
        return BrandRepository.get_by_id(
            db,
            brand_id,
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):
        return {
            "total": BrandRepository.count(
                db,
                organization_id,
            ),
            "items": BrandRepository.get_all(
                db,
                organization_id,
                skip,
                limit,
            ),
        }

    @staticmethod
    def search(
        db: Session,
        organization_id: str,
        keyword: str,
        skip: int = 0,
        limit: int = 20,
    ):
        return BrandRepository.search(
            db,
            organization_id,
            keyword,
            skip,
            limit,
        )

    @staticmethod
    def update(
        db: Session,
        brand_id: str,
        brand_data: BrandUpdate,
        user_id: str,
    ):

        brand = BrandRepository.get_by_id(
            db,
            brand_id,
        )

        if brand is None:
            raise ValueError(
                "Brand not found."
            )

        update_data = brand_data.model_dump(
            exclude_unset=True
        )

        # Prevent duplicate names
        if (
            "name" in update_data
            and update_data["name"] != brand.name
        ):
            duplicate = BrandRepository.get_by_name(
                db,
                brand.organization_id,
                update_data["name"],
            )

            if duplicate:
                raise ValueError(
                    "Brand name already exists."
                )

        for key, value in update_data.items():
            setattr(brand, key, value)

        brand.updated_by = user_id

        return BrandRepository.update(
            db,
            brand,
        )

    @staticmethod
    def delete(
        db: Session,
        brand_id: str,
    ):

        brand = BrandRepository.get_by_id(
            db,
            brand_id,
        )

        if brand is None:
            raise ValueError(
                "Brand not found."
            )

        BrandRepository.delete(
            db,
            brand,
        )

        return {
            "message": "Brand deleted successfully."
        }