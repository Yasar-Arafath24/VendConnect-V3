from pydantic import BaseModel, ConfigDict, EmailStr


class OrganizationCreate(BaseModel):
    organization_name: str
    owner_name: str
    email: EmailStr
    phone: str


class OrganizationResponse(BaseModel):
    id: str
    organization_code: str
    organization_name: str
    owner_name: str
    email: EmailStr
    phone: str
    subscription_plan: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)