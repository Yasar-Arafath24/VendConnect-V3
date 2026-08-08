from sqlalchemy.orm import Session

from app.modules.inventory.movement_model import InventoryMovement


class InventoryMovementRepository:

    # ==========================================
    # Create
    # ==========================================

    @staticmethod
    def create(
        db: Session,
        movement: InventoryMovement,
        commit: bool = True,
    ) -> InventoryMovement:

        db.add(movement)

        if commit:
            db.commit()
            db.refresh(movement)

        return movement

    # ==========================================
    # Get By ID
    # ==========================================

    @staticmethod
    def get_by_id(
        db: Session,
        movement_id: str,
    ):

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.id == movement_id
            )
            .first()
        )

    # ==========================================
    # Get By Inventory
    # ==========================================

    @staticmethod
    def get_by_inventory(
        db: Session,
        organization_id: str,
        inventory_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
                InventoryMovement.inventory_id
                == inventory_id,
            )
            .order_by(
                InventoryMovement.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================
    # Get By Product
    # ==========================================

    @staticmethod
    def get_by_product(
        db: Session,
        organization_id: str,
        product_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
                InventoryMovement.product_id
                == product_id,
            )
            .order_by(
                InventoryMovement.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================
    # Get By Warehouse
    # ==========================================

    @staticmethod
    def get_by_warehouse(
        db: Session,
        organization_id: str,
        warehouse_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
                InventoryMovement.warehouse_id
                == warehouse_id,
            )
            .order_by(
                InventoryMovement.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================
    # Get By Movement Type
    # ==========================================

    @staticmethod
    def get_by_type(
        db: Session,
        organization_id: str,
        movement_type: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
                InventoryMovement.movement_type
                == movement_type,
            )
            .order_by(
                InventoryMovement.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================
    # Get All
    # ==========================================

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
            )
            .order_by(
                InventoryMovement.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================
    # Count
    # ==========================================

    @staticmethod
    def count(
        db: Session,
        organization_id: str,
    ) -> int:

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
            )
            .count()
        )

    # ==========================================
    # Count By Inventory
    # ==========================================

    @staticmethod
    def count_by_inventory(
        db: Session,
        organization_id: str,
        inventory_id: str,
    ) -> int:

        return (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.organization_id
                == organization_id,
                InventoryMovement.inventory_id
                == inventory_id,
            )
            .count()
        )