from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.organizations.repository import OrganizationRepository
from app.modules.warehouses.model import Warehouse
from app.modules.warehouses.repository import WarehouseRepository
from app.modules.warehouses.schema import (
    WarehouseCreate,
    WarehouseUpdate,
)


class WarehouseService:

    @staticmethod
    def create(
        db: Session,
        warehouse_data: WarehouseCreate,
        organization_id: str,
        user_id: str,
    ) -> Warehouse:

        # Validate organization
        organization = OrganizationRepository.get_by_id(
            db,
            organization_id,
        )

        if organization is None:
            raise ValueError(
                "Organization not found."
            )

        # Duplicate name
        if WarehouseRepository.get_by_name(
            db,
            organization_id,
            warehouse_data.name,
        ):
            raise ValueError(
                "Warehouse name already exists."
            )

        # Duplicate code
        if WarehouseRepository.get_by_code(
            db,
            organization_id,
            warehouse_data.code,
        ):
            raise ValueError(
                "Warehouse code already exists."
            )

        # Only one default warehouse
        if warehouse_data.is_default:
            default = WarehouseRepository.get_default(
                db,
                organization_id,
            )

            if default:
                default.is_default = False
                WarehouseRepository.update(
                    db,
                    default,
                )

        warehouse = Warehouse(
            id=str(uuid4()),
            organization_id=organization_id,

            name=warehouse_data.name,
            code=warehouse_data.code,

            address=warehouse_data.address,
            city=warehouse_data.city,
            state=warehouse_data.state,
            country=warehouse_data.country,
            postal_code=warehouse_data.postal_code,

            phone=warehouse_data.phone,
            email=warehouse_data.email,
            manager_name=warehouse_data.manager_name,

            is_default=warehouse_data.is_default,
            is_active=warehouse_data.is_active,

            created_by=user_id,
            updated_by=user_id,
        )

        return WarehouseRepository.create(
            db,
            warehouse,
        )

    @staticmethod
    def get_by_id(
        db: Session,
        warehouse_id: str,
    ):
        return WarehouseRepository.get_by_id(
            db,
            warehouse_id,
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):
        return {
            "total": WarehouseRepository.count(
                db,
                organization_id,
            ),
            "items": WarehouseRepository.get_all(
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
        return WarehouseRepository.search(
            db,
            organization_id,
            keyword,
            skip,
            limit,
        )

    @staticmethod
    def update(
        db: Session,
        warehouse_id: str,
        warehouse_data: WarehouseUpdate,
        user_id: str,
    ):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id,
        )

        if warehouse is None:
            raise ValueError(
                "Warehouse not found."
            )

        update_data = warehouse_data.model_dump(
            exclude_unset=True
        )

        # Validate name
        if (
            "name" in update_data
            and update_data["name"] != warehouse.name
        ):
            duplicate = WarehouseRepository.get_by_name(
                db,
                warehouse.organization_id,
                update_data["name"],
            )

            if duplicate:
                raise ValueError(
                    "Warehouse name already exists."
                )

        # Validate code
        if (
            "code" in update_data
            and update_data["code"] != warehouse.code
        ):
            duplicate = WarehouseRepository.get_by_code(
                db,
                warehouse.organization_id,
                update_data["code"],
            )

            if duplicate:
                raise ValueError(
                    "Warehouse code already exists."
                )

        # Handle default warehouse
        if (
            "is_default" in update_data
            and update_data["is_default"]
        ):
            default = WarehouseRepository.get_default(
                db,
                warehouse.organization_id,
            )

            if default and default.id != warehouse.id:
                default.is_default = False
                WarehouseRepository.update(
                    db,
                    default,
                )

        for key, value in update_data.items():
            setattr(warehouse, key, value)

        warehouse.updated_by = user_id

        return WarehouseRepository.update(
            db,
            warehouse,
        )

    @staticmethod
    def delete(
        db: Session,
        warehouse_id: str,
    ):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id,
        )

        if warehouse is None:
            raise ValueError(
                "Warehouse not found."
            )

        WarehouseRepository.delete(
            db,
            warehouse,
        )

        return {
            "message": "Warehouse deleted successfully."
        }