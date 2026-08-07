from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================
# Base Schema
# ==========================================

class WarehouseBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=30,
    )

    address: str | None = None

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        max_length=100,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    email: EmailStr | None = None

    manager_name: str | None = Field(
        default=None,
        max_length=150,
    )

    is_default: bool = False

    is_active: bool = True


# ==========================================
# Create
# ==========================================

class WarehouseCreate(WarehouseBase):
    pass


# ==========================================
# Update
# ==========================================

class WarehouseUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )

    address: str | None = None

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        max_length=100,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    email: EmailStr | None = None

    manager_name: str | None = Field(
        default=None,
        max_length=150,
    )

    is_default: bool | None = None

    is_active: bool | None = None


# ==========================================
# Response
# ==========================================

class WarehouseResponse(WarehouseBase):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    organization_id: str

    created_by: str | None

    updated_by: str | None

    created_at: datetime

    updated_at: datetime


# ==========================================
# List Response
# ==========================================

class WarehouseListResponse(BaseModel):

    total: int

    items: list[WarehouseResponse]