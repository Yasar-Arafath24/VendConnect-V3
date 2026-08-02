from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    organization_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    password: str
    profile_image: str | None = None


class UserResponse(BaseModel):
    id: str
    organization_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    profile_image: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
