from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.inventory.constants import InventoryMovementType
from app.modules.inventory.movement_model import InventoryMovement
from app.modules.inventory.movement_repository import (
    InventoryMovementRepository,
)


class InventoryMovementService:

    # ==========================================
    # Create Movement
    # ==========================================

    @staticmethod
    def create(
        db: Session,
        organization_id: str,
        inventory_id: str,
        product_id: str,
        warehouse_id: str,
        movement_type: str,
        quantity: int,
        quantity_before: int,
        quantity_after: int,
        user_id: str | None = None,
        reason: str | None = None,
        reference_type: str | None = None,
        reference_id: str | None = None,
        commit: bool = True,
    ) -> InventoryMovement:

        # ==========================================
        # Validate Movement Type
        # ==========================================

        valid_types = {
            InventoryMovementType.STOCK_IN,
            InventoryMovementType.STOCK_OUT,
            InventoryMovementType.ADJUSTMENT_IN,
            InventoryMovementType.ADJUSTMENT_OUT,
            InventoryMovementType.TRANSFER_IN,
            InventoryMovementType.TRANSFER_OUT,
            InventoryMovementType.PURCHASE,
            InventoryMovementType.SALE,
            InventoryMovementType.RETURN_IN,
            InventoryMovementType.RETURN_OUT,
        }

        if movement_type not in valid_types:
            raise ValueError(
                f"Invalid inventory movement type: {movement_type}"
            )

        # ==========================================
        # Validate Quantities
        # ==========================================

        if quantity == 0:
            raise ValueError(
                "Movement quantity cannot be zero."
            )

        if quantity_before < 0:
            raise ValueError(
                "Quantity before movement cannot be negative."
            )

        if quantity_after < 0:
            raise ValueError(
                "Quantity after movement cannot be negative."
            )

        # ==========================================
        # Validate Quantity Mathematics
        # ==========================================

        if quantity_before + quantity != quantity_after:
            raise ValueError(
                "Invalid movement quantities: "
                "quantity_before + quantity must equal quantity_after."
            )

        # ==========================================
        # Validate Direction
        # ==========================================

        inbound_types = {
            InventoryMovementType.STOCK_IN,
            InventoryMovementType.ADJUSTMENT_IN,
            InventoryMovementType.TRANSFER_IN,
            InventoryMovementType.PURCHASE,
            InventoryMovementType.RETURN_IN,
        }

        outbound_types = {
            InventoryMovementType.STOCK_OUT,
            InventoryMovementType.ADJUSTMENT_OUT,
            InventoryMovementType.TRANSFER_OUT,
            InventoryMovementType.SALE,
            InventoryMovementType.RETURN_OUT,
        }

        if movement_type in inbound_types and quantity <= 0:
            raise ValueError(
                "Inbound movement quantity must be positive."
            )

        if movement_type in outbound_types and quantity >= 0:
            raise ValueError(
                "Outbound movement quantity must be negative."
            )

        # ==========================================
        # Create Movement
        # ==========================================

        movement = InventoryMovement(
            id=str(uuid4()),

            organization_id=organization_id,

            inventory_id=inventory_id,

            product_id=product_id,

            warehouse_id=warehouse_id,

            movement_type=movement_type,

            quantity=quantity,

            quantity_before=quantity_before,

            quantity_after=quantity_after,

            reference_type=reference_type,

            reference_id=reference_id,

            reason=reason,

            created_by=user_id,
        )

        return InventoryMovementRepository.create(
            db=db,
            movement=movement,
            commit=commit,
        )

    # ==========================================
    # Get By ID
    # ==========================================

    @staticmethod
    def get_by_id(
        db: Session,
        movement_id: str,
        organization_id: str,
    ):

        movement = InventoryMovementRepository.get_by_id(
            db,
            movement_id,
        )

        if movement is None:
            return None

        if movement.organization_id != organization_id:
            return None

        return movement

    # ==========================================
    # Inventory History
    # ==========================================

    @staticmethod
    def get_by_inventory(
        db: Session,
        organization_id: str,
        inventory_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return {
            "total": (
                InventoryMovementRepository
                .count_by_inventory(
                    db,
                    organization_id,
                    inventory_id,
                )
            ),
            "items": (
                InventoryMovementRepository
                .get_by_inventory(
                    db,
                    organization_id,
                    inventory_id,
                    skip,
                    limit,
                )
            ),
        }

    # ==========================================
    # Product History
    # ==========================================

    @staticmethod
    def get_by_product(
        db: Session,
        organization_id: str,
        product_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return InventoryMovementRepository.get_by_product(
            db,
            organization_id,
            product_id,
            skip,
            limit,
        )

    # ==========================================
    # Warehouse History
    # ==========================================

    @staticmethod
    def get_by_warehouse(
        db: Session,
        organization_id: str,
        warehouse_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return InventoryMovementRepository.get_by_warehouse(
            db,
            organization_id,
            warehouse_id,
            skip,
            limit,
        )

    # ==========================================
    # Movement Type History
    # ==========================================

    @staticmethod
    def get_by_type(
        db: Session,
        organization_id: str,
        movement_type: str,
        skip: int = 0,
        limit: int = 20,
    ):

        valid_types = {
            InventoryMovementType.STOCK_IN,
            InventoryMovementType.STOCK_OUT,
            InventoryMovementType.ADJUSTMENT_IN,
            InventoryMovementType.ADJUSTMENT_OUT,
            InventoryMovementType.TRANSFER_IN,
            InventoryMovementType.TRANSFER_OUT,
            InventoryMovementType.PURCHASE,
            InventoryMovementType.SALE,
            InventoryMovementType.RETURN_IN,
            InventoryMovementType.RETURN_OUT,
        }

        if movement_type not in valid_types:
            raise ValueError(
                f"Invalid inventory movement type: {movement_type}"
            )

        return InventoryMovementRepository.get_by_type(
            db,
            organization_id,
            movement_type,
            skip,
            limit,
        )

    # ==========================================
    # Organization History
    # ==========================================

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return {
            "total": InventoryMovementRepository.count(
                db,
                organization_id,
            ),
            "items": InventoryMovementRepository.get_all(
                db,
                organization_id,
                skip,
                limit,
            ),
        }