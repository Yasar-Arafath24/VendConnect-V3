def test_inventory_summary_imports():

    from app.modules.inventory.summary_repository import (
        InventorySummaryRepository,
    )

    from app.modules.inventory.summary_service import (
        InventorySummaryService,
    )

    assert InventorySummaryRepository is not None
    assert InventorySummaryService is not None