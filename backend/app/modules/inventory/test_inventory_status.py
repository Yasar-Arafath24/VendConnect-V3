from app.modules.inventory.constants import (
    InventoryStatus,
)

from app.modules.inventory.status_service import (
    InventoryStatusService,
)


def test_out_of_stock():

    result = InventoryStatusService.classify(
        quantity=0,
        reorder_level=10,
        max_stock_level=100,
    )

    assert result == InventoryStatus.OUT_OF_STOCK