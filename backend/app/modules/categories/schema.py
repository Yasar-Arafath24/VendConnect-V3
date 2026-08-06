from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base Schema
# ==========================================

class CategoryBase(BaseModel):
    parent_id: str | None = None

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: str | None = None

    is_active: bool = True


# ==========================================
# Create
# ==========================================

class CategoryCreate(CategoryBase):
    pass


# ==========================================
# Update
# ==========================================

class CategoryUpdate(BaseModel):

    parent_id: str | None = None

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = None

    is_active: bool | None = None


# ==========================================
# Response
# ==========================================

class CategoryResponse(CategoryBase):

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
# Tree Response
# ==========================================

class CategoryTreeResponse(BaseModel):

    id: str

    name: str

    children: list["CategoryTreeResponse"] = []

    model_config = ConfigDict(
        from_attributes=True,
    )


CategoryTreeResponse.model_rebuild()


# ==========================================
# List Response
# ==========================================

class CategoryListResponse(BaseModel):

    total: int

    items: list[CategoryResponse]