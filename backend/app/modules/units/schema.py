from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base Schema
# ==========================================

class UnitBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    symbol: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )

    description: str | None = None

    is_active: bool = True


# ==========================================
# Create
# ==========================================

class UnitCreate(UnitBase):
    pass


# ==========================================
# Update
# ==========================================

class UnitUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    symbol: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    description: str | None = None

    is_active: bool | None = None


# ==========================================
# Response
# ==========================================

class UnitResponse(UnitBase):

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

class UnitListResponse(BaseModel):

    total: int

    items: list[UnitResponse]