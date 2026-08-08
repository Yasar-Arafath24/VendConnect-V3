def test_inventory_classification():

    from app.modules.inventory.constants import (
        InventoryStatus,
    )

    from app.modules.inventory.status_service import (
        InventoryStatusService,
    )

    class FakeInventory:
        quantity = 5
        reorder_level = 10
        max_stock_level = 100

    result = (
        InventoryStatusService
        .classify_inventory(
            FakeInventory()
        )
    )

    assert result == InventoryStatus.LOW_STOCK


def test_out_of_stock():

    from app.modules.inventory.constants import (
        InventoryStatus,
    )

    from app.modules.inventory.status_service import (
        InventoryStatusService,
    )

    result = InventoryStatusService.classify(
        quantity=0,
        reorder_level=10,
        max_stock_level=100,
    )

    assert result == InventoryStatus.OUT_OF_STOCK


def test_low_stock_boundary():

    from app.modules.inventory.constants import (
        InventoryStatus,
    )

    from app.modules.inventory.status_service import (
        InventoryStatusService,
    )

    result = InventoryStatusService.classify(
        quantity=10,
        reorder_level=10,
        max_stock_level=100,
    )

    assert result == InventoryStatus.LOW_STOCK


def test_healthy():

    from app.modules.inventory.constants import (
        InventoryStatus,
    )

    from app.modules.inventory.status_service import (
        InventoryStatusService,
    )

    result = InventoryStatusService.classify(
        quantity=50,
        reorder_level=10,
        max_stock_level=100,
    )

    assert result == InventoryStatus.HEALTHY


def test_overstocked():

    from app.modules.inventory.constants import (
        InventoryStatus,
    )

    from app.modules.inventory.status_service import (
        InventoryStatusService,
    )

    result = InventoryStatusService.classify(
        quantity=150,
        reorder_level=10,
        max_stock_level=100,
    )

    assert result == InventoryStatus.OVERSTOCKED


def test_unlimited_max_stock_never_overstocked():

    from app.modules.inventory.constants import (
        InventoryStatus,
    )

    from app.modules.inventory.status_service import (
        InventoryStatusService,
    )

    result = InventoryStatusService.classify(
        quantity=1000000,
        reorder_level=10,
        max_stock_level=0,
    )

    assert result == InventoryStatus.HEALTHY
