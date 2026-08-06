from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.organizations.repository import OrganizationRepository
from app.modules.units.model import Unit
from app.modules.units.repository import UnitRepository
from app.modules.units.schema import (
    UnitCreate,
    UnitUpdate,
)


class UnitService:

    @staticmethod
    def create(
        db: Session,
        unit_data: UnitCreate,
        organization_id: str,
        user_id: str,
    ) -> Unit:

        # Validate organization
        organization = OrganizationRepository.get_by_id(
            db,
            organization_id,
        )

        if organization is None:
            raise ValueError(
                "Organization not found."
            )

        # Prevent duplicate name
        existing_name = UnitRepository.get_by_name(
            db,
            organization_id,
            unit_data.name,
        )

        if existing_name:
            raise ValueError(
                "Unit name already exists."
            )

        # Prevent duplicate symbol
        existing_symbol = UnitRepository.get_by_symbol(
            db,
            organization_id,
            unit_data.symbol,
        )

        if existing_symbol:
            raise ValueError(
                "Unit symbol already exists."
            )

        unit = Unit(
            id=str(uuid4()),
            organization_id=organization_id,

            name=unit_data.name,
            symbol=unit_data.symbol,
            description=unit_data.description,
            is_active=unit_data.is_active,

            created_by=user_id,
            updated_by=user_id,
        )

        return UnitRepository.create(
            db,
            unit,
        )

    @staticmethod
    def get_by_id(
        db: Session,
        unit_id: str,
    ):
        return UnitRepository.get_by_id(
            db,
            unit_id,
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):
        return {
            "total": UnitRepository.count(
                db,
                organization_id,
            ),
            "items": UnitRepository.get_all(
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
        return UnitRepository.search(
            db,
            organization_id,
            keyword,
            skip,
            limit,
        )

    @staticmethod
    def update(
        db: Session,
        unit_id: str,
        unit_data: UnitUpdate,
        user_id: str,
    ):

        unit = UnitRepository.get_by_id(
            db,
            unit_id,
        )

        if unit is None:
            raise ValueError(
                "Unit not found."
            )

        update_data = unit_data.model_dump(
            exclude_unset=True
        )

        # Validate name uniqueness
        if (
            "name" in update_data
            and update_data["name"] != unit.name
        ):
            duplicate = UnitRepository.get_by_name(
                db,
                unit.organization_id,
                update_data["name"],
            )

            if duplicate:
                raise ValueError(
                    "Unit name already exists."
                )

        # Validate symbol uniqueness
        if (
            "symbol" in update_data
            and update_data["symbol"] != unit.symbol
        ):
            duplicate = UnitRepository.get_by_symbol(
                db,
                unit.organization_id,
                update_data["symbol"],
            )

            if duplicate:
                raise ValueError(
                    "Unit symbol already exists."
                )

        for key, value in update_data.items():
            setattr(unit, key, value)

        unit.updated_by = user_id

        return UnitRepository.update(
            db,
            unit,
        )

    @staticmethod
    def delete(
        db: Session,
        unit_id: str,
    ):

        unit = UnitRepository.get_by_id(
            db,
            unit_id,
        )

        if unit is None:
            raise ValueError(
                "Unit not found."
            )

        UnitRepository.delete(
            db,
            unit,
        )

        return {
            "message": "Unit deleted successfully."
        }