from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Movement Response
# ==========================================

class InventoryMovementResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    organization_id: str

    inventory_id: str

    product_id: str

    warehouse_id: str

    movement_type: str

    quantity: int

    quantity_before: int

    quantity_after: int

    reference_type: str | None = None

    reference_id: str | None = None

    reason: str | None = None

    created_by: str | None = None

    created_at: datetime


# ==========================================
# Movement List Response
# ==========================================

class InventoryMovementListResponse(BaseModel):

    total: int

    items: list[InventoryMovementResponse]


# ==========================================
# Movement Filter
# ==========================================

class InventoryMovementFilter(BaseModel):

    movement_type: str | None = None

    product_id: str | None = None

    warehouse_id: str | None = None

    inventory_id: str | None = None

    skip: int = Field(
        default=0,
        ge=0,
    )

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )