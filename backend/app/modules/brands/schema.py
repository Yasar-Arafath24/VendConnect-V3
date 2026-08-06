from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base Schema
# ==========================================

class BrandBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: str | None = None

    logo_url: str | None = Field(
        default=None,
        max_length=500,
    )

    is_active: bool = True


# ==========================================
# Create
# ==========================================

class BrandCreate(BrandBase):
    pass


# ==========================================
# Update
# ==========================================

class BrandUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = None

    logo_url: str | None = Field(
        default=None,
        max_length=500,
    )

    is_active: bool | None = None


# ==========================================
# Response
# ==========================================

class BrandResponse(BrandBase):

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

class BrandListResponse(BaseModel):

    total: int

    items: list[BrandResponse]