from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base Schema
# ==========================================

class ProductBase(BaseModel):
    category_id: str | None = None
    brand_id: str | None = None
    unit_id: str | None = None

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    cost_price: Decimal = Field(
        ...,
        gt=0,
    )

    selling_price: Decimal = Field(
        ...,
        gt=0,
    )

    stock: int = Field(
        default=0,
        ge=0,
    )

    minimum_stock: int = Field(
        default=0,
        ge=0,
    )

    barcode: str | None = None

    is_active: bool = True


# ==========================================
# Create
# ==========================================

class ProductCreate(ProductBase):
    pass


# ==========================================
# Update
# ==========================================

class ProductUpdate(BaseModel):

    category_id: str | None = None
    brand_id: str | None = None
    unit_id: str | None = None

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    cost_price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    selling_price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    stock: int | None = Field(
        default=None,
        ge=0,
    )

    minimum_stock: int | None = Field(
        default=None,
        ge=0,
    )

    barcode: str | None = None

    is_active: bool | None = None


# ==========================================
# Response
# ==========================================

class ProductResponse(ProductBase):

    model_config = ConfigDict(from_attributes=True)

    id: str
    organization_id: str

    sku: str

    created_by: str | None
    updated_by: str | None

    created_at: datetime
    updated_at: datetime


# ==========================================
# List Response
# ==========================================

class ProductListResponse(BaseModel):

    total: int

    items: list[ProductResponse]