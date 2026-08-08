from app.modules.inventory.constants import (
    InventoryStatus,
)


class InventoryStatusService:

    @staticmethod
    def classify(
        quantity: int,
        reorder_level: int,
        max_stock_level: int,
    ) -> InventoryStatus:

        # ==========================================
        # Out Of Stock
        # ==========================================

        if quantity == 0:
            return InventoryStatus.OUT_OF_STOCK

        # ==========================================
        # Low Stock
        # ==========================================

        if quantity <= reorder_level:
            return InventoryStatus.LOW_STOCK

        # ==========================================
        # Overstocked
        # ==========================================

        if (
            max_stock_level > 0
            and quantity > max_stock_level
        ):
            return InventoryStatus.OVERSTOCKED

        # ==========================================
        # Healthy
        # ==========================================

        return InventoryStatus.HEALTHY