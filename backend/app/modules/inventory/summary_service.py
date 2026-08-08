from sqlalchemy.orm import Session

from app.modules.inventory.summary_repository import (
    InventorySummaryRepository,
)


class InventorySummaryService:

    @staticmethod
    def get_summary(
        db: Session,
        organization_id: str,
    ):

        summary = (
            InventorySummaryRepository
            .get_summary(
                db=db,
                organization_id=organization_id,
            )
        )

        total_available_quantity = (
            summary["total_quantity"]
            - summary["total_reserved_quantity"]
        )

        return {
            "inventory_count": (
                summary["inventory_count"]
            ),

            "total_quantity": (
                summary["total_quantity"]
            ),

            "total_reserved_quantity": (
                summary[
                    "total_reserved_quantity"
                ]
            ),

            "total_available_quantity": (
                total_available_quantity
            ),

            # Pricing will be added after
            # verifying the project's Product
            # pricing model.
            "total_inventory_value": 0.0,

            "low_stock_count": (
                summary["low_stock_count"]
            ),

            "out_of_stock_count": (
                summary["out_of_stock_count"]
            ),
        }