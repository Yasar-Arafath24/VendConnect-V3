from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.inventory.model import Inventory


class InventorySummaryRepository:

    @staticmethod
    def get_summary(
        db: Session,
        organization_id: str,
    ):
        result = (
            db.query(
                func.count(Inventory.id).label(
                    "inventory_count"
                ),
                func.coalesce(
                    func.sum(Inventory.quantity),
                    0,
                ).label(
                    "total_quantity"
                ),
                func.coalesce(
                    func.sum(
                        Inventory.reserved_quantity
                    ),
                    0,
                ).label(
                    "total_reserved_quantity"
                ),
            )
            .filter(
                Inventory.organization_id
                == organization_id
            )
            .one()
        )

        low_stock_count = (
            db.query(
                func.count(Inventory.id)
            )
            .filter(
                Inventory.organization_id
                == organization_id
            )
            .filter(
                Inventory.quantity
                <= Inventory.reorder_level
            )
            .filter(
                Inventory.quantity > 0
            )
            .scalar()
        )

        out_of_stock_count = (
            db.query(
                func.count(Inventory.id)
            )
            .filter(
                Inventory.organization_id
                == organization_id
            )
            .filter(
                Inventory.quantity == 0
            )
            .scalar()
        )

        return {
            "inventory_count": result.inventory_count,
            "total_quantity": result.total_quantity,
            "total_reserved_quantity": (
                result.total_reserved_quantity
            ),
            "low_stock_count": low_stock_count or 0,
            "out_of_stock_count": (
                out_of_stock_count or 0
            ),
        }