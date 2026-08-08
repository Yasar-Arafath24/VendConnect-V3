from sqlalchemy.orm import Session

from app.modules.inventory.model import Inventory


class InventoryQueryRepository:

    @staticmethod
    def search(
        db: Session,
        organization_id: str,
        product_id: str | None = None,
        warehouse_id: str | None = None,
        min_quantity: int | None = None,
        max_quantity: int | None = None,
        low_stock_only: bool = False,
        out_of_stock_only: bool = False,
        skip: int = 0,
        limit: int = 20,
    ):

        query = (
            db.query(Inventory)
            .filter(
                Inventory.organization_id
                == organization_id
            )
        )

        # ==========================================
        # Product Filter
        # ==========================================

        if product_id is not None:

            query = query.filter(
                Inventory.product_id
                == product_id
            )

        # ==========================================
        # Warehouse Filter
        # ==========================================

        if warehouse_id is not None:

            query = query.filter(
                Inventory.warehouse_id
                == warehouse_id
            )

        # ==========================================
        # Minimum Quantity
        # ==========================================

        if min_quantity is not None:

            query = query.filter(
                Inventory.quantity
                >= min_quantity
            )

        # ==========================================
        # Maximum Quantity
        # ==========================================

        if max_quantity is not None:

            query = query.filter(
                Inventory.quantity
                <= max_quantity
            )

        # ==========================================
        # Out Of Stock
        # ==========================================

        if out_of_stock_only:

            query = query.filter(
                Inventory.quantity == 0
            )

        # ==========================================
        # Low Stock
        # ==========================================

        elif low_stock_only:

            query = query.filter(
                Inventory.quantity
                <= Inventory.reorder_level
            )

            query = query.filter(
                Inventory.quantity > 0
            )

        # ==========================================
        # Count
        # ==========================================

        total = query.count()

        # ==========================================
        # Pagination
        # ==========================================

        items = (
            query
            .order_by(
                Inventory.updated_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        return total, items