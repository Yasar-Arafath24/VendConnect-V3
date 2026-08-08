from sqlalchemy.orm import Session

from app.modules.inventory.query_repository import (
    InventoryQueryRepository,
)
from app.modules.inventory.status_service import (
    InventoryStatusService,
)


class InventoryQueryService:

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

        # ==========================================
        # Validate Quantity Range
        # ==========================================

        if (
            min_quantity is not None
            and max_quantity is not None
            and min_quantity > max_quantity
        ):
            raise ValueError(
                "Minimum quantity cannot be greater than maximum quantity."
            )

        # ==========================================
        # Validate Stock Status Filters
        # ==========================================

        if low_stock_only and out_of_stock_only:
            raise ValueError(
                "Low-stock and out-of-stock filters cannot be used together."
            )

        # ==========================================
        # Validate Pagination
        # ==========================================

        if skip < 0:
            raise ValueError(
                "Skip cannot be negative."
            )

        if limit < 1 or limit > 100:
            raise ValueError(
                "Limit must be between 1 and 100."
            )

        # ==========================================
        # Execute Search
        # ==========================================

        total, items = InventoryQueryRepository.search(
            db=db,
            organization_id=organization_id,
            product_id=product_id,
            warehouse_id=warehouse_id,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            low_stock_only=low_stock_only,
            out_of_stock_only=out_of_stock_only,
            skip=skip,
            limit=limit,
        )

        # ==========================================
        # Enrich With Computed Status
        # ==========================================

        for item in items:

            item.status = (
                InventoryStatusService
                .classify_inventory(item)
            )

        return {
            "total": total,
            "items": items,
        }