from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base Schema
# ==========================================

class InventoryBase(BaseModel):

    warehouse_id: str

    product_id: str

    quantity: int = Field(
        default=0,
        ge=0,
    )

    reserved_quantity: int = Field(
        default=0,
        ge=0,
    )

    reorder_level: int = Field(
        default=0,
        ge=0,
    )

    max_stock_level: int = Field(
        default=0,
        ge=0,
    )


# ==========================================
# Create
# ==========================================

class InventoryCreate(InventoryBase):
    pass


# ==========================================
# Update
# ==========================================

class InventoryUpdate(BaseModel):

    quantity: int | None = Field(
        default=None,
        ge=0,
    )

    reserved_quantity: int | None = Field(
        default=None,
        ge=0,
    )

    reorder_level: int | None = Field(
        default=None,
        ge=0,
    )

    max_stock_level: int | None = Field(
        default=None,
        ge=0,
    )


# ==========================================
# Stock Adjustment
# ==========================================

class StockAdjustment(BaseModel):

    quantity: int

    reason: str = Field(
        ...,
        min_length=3,
        max_length=255,
    )


# ==========================================
# Stock Transfer
# ==========================================

class StockTransfer(BaseModel):

    from_warehouse_id: str

    to_warehouse_id: str

    product_id: str

    quantity: int = Field(
        ...,
        gt=0,
    )

    reason: str | None = Field(
        default=None,
        max_length=255,
    )


# ==========================================
# Query / Filter
# ==========================================

class InventoryFilter(BaseModel):

    product_id: str | None = None

    warehouse_id: str | None = None

    min_quantity: int | None = Field(
        default=None,
        ge=0,
    )

    max_quantity: int | None = Field(
        default=None,
        ge=0,
    )

    low_stock_only: bool = False

    out_of_stock_only: bool = False

    skip: int = Field(
        default=0,
        ge=0,
    )

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )


# ==========================================
# Response
# ==========================================

class InventoryResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    organization_id: str

    warehouse_id: str

    product_id: str

    quantity: int

    reserved_quantity: int

    reorder_level: int

    max_stock_level: int

    available_quantity: int

    created_by: str | None

    updated_by: str | None

    created_at: datetime

    updated_at: datetime


# ==========================================
# List Response
# ==========================================

class InventoryListResponse(BaseModel):

    total: int

    items: list[InventoryResponse]
    
    
class InventorySummaryResponse(BaseModel):

    inventory_count: int

    total_quantity: int

    total_reserved_quantity: int

    total_available_quantity: int

    total_inventory_value: float

    low_stock_count: int

    out_of_stock_count: int