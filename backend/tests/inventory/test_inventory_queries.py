def test_inventory_query_module_imports():
    from app.modules.inventory.query_repository import (
        InventoryQueryRepository,
    )

    from app.modules.inventory.query_service import (
        InventoryQueryService,
    )

    assert InventoryQueryRepository is not None
    assert InventoryQueryService is not None